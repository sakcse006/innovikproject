from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging


class OpAdmissionRegisterMember(models.Model):
    _name = 'op.admission.register.member'
    _description = 'Admission Register Member'

    name = fields.Char(string='Name',store=True, required=True, readonly=True,default='/',
        states={'draft': [('readonly', True)]})
    start_date = fields.Date(
        'Start Date', required=True, readonly=True,
        default=fields.Date.today(), states={'draft': [('readonly', False)]})
    end_date = fields.Date(
        'End Date', required=True, readonly=True,
        default=(datetime.today() + relativedelta(days=30)),
        states={'draft': [('readonly', False)]})
    district_id = fields.Many2one(
        'op.district', 'District', required=True, readonly=True,
        states={'draft': [('readonly', False)]}, track_visibility='onchange')
    min_count = fields.Integer(
        'Minimum No. of Admission', readonly=True,
        states={'draft': [('readonly', False)]})
    max_count = fields.Integer(
        'Maximum No. of Admission', readonly=True,
        states={'draft': [('readonly', False)]}, default=30)
    admission_ids = fields.One2many(
        'op.admission.member', 'register_id', 'Admissions')
    state = fields.Selection(
        [('draft', 'Draft'),('cancel', 'Cancelled'),
         ('admission', 'Admission Process'), ('done', 'Done')],
        'Status', default='draft', track_visibility='onchange')
    union_id = fields.Many2one(
        'op.union', 'Union', required=False,readonly=True, domain="[('district_id','=',district_id)]",
        states={'draft': [('readonly', False)]})
    panchayat_id = fields.Many2one(
        'op.panchayat', 'Panchayat', required=False,readonly=True, domain="[('union_id','=',union_id)]",
        states={'draft': [('readonly', False)]})

    @api.onchange('district_id')
    def onchange_district(self):
        self.union_id = False
        self.panchayat_id = False
        self.user_id = False

    @api.onchange('union_id')
    def onchange_union(self):
        self.panchayat_id = False
        self.user_id = False

    @api.onchange('panchayat_id')
    def onchange_panchayat(self):
        self.user_id = False

    @api.onchange('district_id', 'union_id', 'panchayat_id')
    def onchange_member(self):
        for register in self:
            if register.district_id and not register.union_id and not register.panchayat_id:
                users = self.env.ref('common_custom_membership.group_op_district_admin').users.ids
                user_list = []
                for user in users:
                    admission = self.env['op.admission.register.member'].search([('user_id','=',user),('state','!=','done')])
                    if not admission:
                        user_list.append(user)
                return {'domain': {'user_id': [('id', 'in', user_list)]}}
            elif register.district_id and register.union_id and not register.panchayat_id:
                users = self.env.ref('common_custom_membership.group_op_union_admin').users.ids
                user_list = []
                for user in users:
                    admission = self.env['op.admission.register.member'].search([('user_id', '=', user),('state', '!=', 'done')])
                    if not admission:
                        user_list.append(user)
                return {'domain': {'user_id': [('id', 'in', user_list)]}}
            elif register.district_id and register.union_id and register.panchayat_id:
                users = self.env.ref('common_custom_membership.group_op_panchayat_admin').users.ids
                user_list = []
                for user in users:
                    admission = self.env['op.admission.register.member'].search([('user_id', '=', user),('state', '!=', 'done')])
                    if not admission:
                        user_list.append(user)
                return {'domain': {'user_id': [('id', 'in', user_list)]}}

    user_id = fields.Many2one('res.users', string='User',required=True, readonly=False,
                              states={'done': [('readonly', True)]})

    @api.model
    def create(self, vals):
        logging.info(vals)
        district_name = ''
        union_name = ''
        panchayat_name = ''
        if vals.get('district_id'):
           district_name = self.env['op.district'].browse(vals.get('district_id')).district_name
        if vals.get('union_id'):
           union_name = self.env['op.union'].browse(vals.get('union_id')).union_name
        if vals.get('panchayat_id'):
           panchayat_name = self.env['op.panchayat'].browse(vals.get('panchayat_id')).panchayat_name
        name = district_name
        if union_name:
            name +=str('-')+ union_name
        if panchayat_name:
            name += str('-') +panchayat_name
        logging.info(name)
        vals['name'] = name
        res = super(OpAdmissionRegisterMember, self).create(vals)
        return res

    @api.multi
    @api.constrains('start_date', 'end_date')
    def check_dates(self):
        for record in self:
            start_date = fields.Date.from_string(record.start_date)
            end_date = fields.Date.from_string(record.end_date)
            if start_date > end_date:
                raise ValidationError(_("End Date cannot be set before \
                Start Date."))

    @api.multi
    @api.constrains('min_count', 'max_count')
    def check_no_of_admission(self):
        for record in self:
            if (record.min_count < 0) or (record.max_count < 0):
                raise ValidationError(_("No of Admission should be positive!"))
            if record.min_count > record.max_count:
                raise ValidationError(_(
                    "Min Admission can't be greater than Max Admission"))

    @api.multi
    def set_to_draft(self):
        self.state = 'draft'

    @api.multi
    def cancel_register(self):
        self.state = 'cancel'

    @api.multi
    def start_admission(self):
        self.state = 'admission'

    @api.multi
    def close_register(self):
        self.state = 'done'
