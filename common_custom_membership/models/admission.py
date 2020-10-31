from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import logging


class OpAdmissionMember(models.Model):
    _name = 'op.admission.member'
    # _inherit = 'mail.thread'
    _rec_name = 'application_number'
    _order = "application_number desc"
    _description = "Admission Member"

    name = fields.Char(
        'First Name', size=128, required=True,
        states={'done': [('readonly', True)]})
    middle_name = fields.Char(
        'Middle Name', size=128,
        states={'done': [('readonly', True)]})
    last_name = fields.Char(
        'Last Name', size=128, required=True,
        states={'done': [('readonly', True)]})
    title = fields.Many2one(
        'res.partner.title', 'Title', states={'done': [('readonly', True)]})
    application_number = fields.Char(
        'Application Number', size=16, required=True, copy=False,
        states={'done': [('readonly', True)]},
        default=lambda self:
        self.env['ir.sequence'].next_by_code('op.admission.member'))
    admission_date = fields.Date(
        'Admission Date', copy=False,
        states={'done': [('readonly', True)]})
    application_date = fields.Datetime(
        'Application Date', required=True, copy=False,
        states={'done': [('readonly', True)]},
        default=lambda self: fields.Datetime.now())
    birth_date = fields.Date(
        'Birth Date', required=True, states={'done': [('readonly', True)]})
    district_id = fields.Many2one(
        'op.district', 'District', required=True,readonly=True,related='register_id.district_id',
        states={'done': [('readonly', True)]})
    union_id = fields.Many2one(
        'op.union', 'Union', required=False,readonly=True,domain="[('district_id','=',district_id)]",
        related='register_id.union_id',states={'done': [('readonly', True)]})
    panchayat_id = fields.Many2one(
        'op.panchayat', 'Panchayat', required=False,readonly=True,domain="[('union_id','=',union_id)]",
        related='register_id.panchayat_id',states={'done': [('readonly', True)]})
    street = fields.Char(
        'Street', size=256, states={'done': [('readonly', True)]})
    street2 = fields.Char(
        'Street2', size=256, states={'done': [('readonly', True)]})
    phone = fields.Char(
        'Phone', size=16, states={'done': [('readonly', True)]})
    mobile = fields.Char(
        'Mobile', size=16, states={'done': [('readonly', True)]})
    email = fields.Char(
        'Email', size=256, required=True,
        states={'done': [('readonly', True)]})
    city = fields.Char('City', size=64, states={'done': [('readonly', True)]})
    zip = fields.Char('Zip', size=8, states={'done': [('readonly', True)]})
    state_id = fields.Many2one(
        'res.country.state', 'States', states={'done': [('readonly', True)]})
    country_id = fields.Many2one(
        'res.country', 'Country', states={'done': [('readonly', True)]})
    image = fields.Binary('image', states={'done': [('readonly', True)]})
    state = fields.Selection(
        [('draft', 'Draft'), ('submit', 'Submitted'),
         ('admission', 'Admission Confirm'),
         ('cancel', 'Cancelled'), ('done', 'Done')],
        'State', default='draft', track_visibility='onchange')
    gender = fields.Selection(
        [('m', 'Male'), ('f', 'Female'), ('o', 'Other')], 'Gender',
        required=True, states={'done': [('readonly', True)]})
    member_id = fields.Many2one(
        'op.member', 'Member', states={'done': [('readonly', True)]})
    nbr = fields.Integer('No of Admission', readonly=True)
    register_id = fields.Many2one(
        'op.admission.register.member', 'Admission Register', required=True,
        states={'done': [('readonly', True)]})
    partner_id = fields.Many2one('res.partner', 'Partner')
    is_member = fields.Boolean('Is Already Member',states={'done': [('readonly', True)]})
    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user, readonly=True)
    blood_group = fields.Selection(
        [('A+', 'A+ve'), ('B+', 'B+ve'), ('O+', 'O+ve'), ('AB+', 'AB+ve'),
         ('A-', 'A-ve'), ('B-', 'B-ve'), ('O-', 'O-ve'), ('AB-', 'AB-ve')],
        'Blood Group')
    nationality = fields.Many2one('res.country', 'Nationality')
    emergency_contact = fields.Many2one(
        'res.partner', 'Emergency Contact')

    @api.onchange('member_id', 'is_member')
    def onchange_student(self):
        if self.is_member and self.member_id:
            member = self.member_id
            self.title = member.title and member.title.id or False
            self.name = member.name
            self.middle_name = member.middle_name
            self.last_name = member.last_name
            self.birth_date = member.birth_date
            self.gender = member.gender
            self.blood_group = member.blood_group
            self.nationality = member.nationality and \
                member.nationality.id or False
            self.emergency_contact = member.emergency_contact and \
                member.emergency_contact.id or False
            self.image = member.image or False
            self.street = member.street or False
            self.street2 = member.street2 or False
            self.phone = member.phone or False
            self.mobile = member.mobile or False
            self.email = member.email or False
            self.zip = member.zip or False
            self.city = member.city or False
            self.country_id = member.country_id and \
                member.country_id.id or False
            self.state_id = member.state_id and \
                member.state_id.id or False
            self.partner_id = member.partner_id and \
                member.partner_id.id or False
        else:
            self.title = ''
            self.name = ''
            self.middle_name = ''
            self.last_name = ''
            self.birth_date = ''
            self.gender = ''
            self.blood_group = ''
            self.nationality = False
            self.emergency_contact = False
            self.image = False
            self.street = ''
            self.street2 = ''
            self.phone = ''
            self.mobile = ''
            self.email = ''
            self.zip = ''
            self.city = ''
            self.country_id = False
            self.state_id = False
            self.partner_id = False

    # @api.onchange('district_id')
    # def onchange_district(self):
    #     self.union_id = False
    #     self.panchayat_id = False
    #
    # @api.onchange('union_id')
    # def onchange_union(self):
    #     self.panchayat_id = False

    @api.multi
    @api.constrains('register_id', 'application_date')
    def _check_admission_register(self):
        for record in self:
            start_date = fields.Date.from_string(record.register_id.start_date)
            end_date = fields.Date.from_string(record.register_id.end_date)
            application_date = fields.Date.from_string(record.application_date)
            if application_date < start_date or application_date > end_date:
                raise ValidationError(_(
                    "Application Date should be between Start Date & \
                    End Date of Admission Register."))

    @api.multi
    @api.constrains('birth_date')
    def _check_birthdate(self):
        for record in self:
            if record.birth_date > fields.Date.today():
                raise ValidationError(_(
                    "Birth Date can't be greater than current date!"))

    @api.multi
    def submit_form(self):
        self.state = 'submit'

    @api.multi
    def admission_confirm(self):
        logging.info('1.......')
        for record in self:
            if not record.partner_id:
                partner_id = self.env['res.partner'].create({
                    'name': record.name
                })
                record.partner_id = partner_id.id
            record.state = 'admission'

    @api.multi
    def get_student_vals(self):
        for member in self:
            return {
                'title': member.title and member.title.id or False,
                'name': member.name,
                'middle_name': member.middle_name,
                'last_name': member.last_name,
                'birth_date': member.birth_date,
                'gender': member.gender,
                'blood_group': member.blood_group,
                'nationality': member.nationality and member.nationality.id or False,
                'emergency_contact': member.emergency_contact and member.emergency_contact.id or False,
                'district_id':
                member.district_id and member.district_id.id or False,
                'union_id':
                member.union_id and member.union_id.id or False,
                'panchayat_id':
                    member.panchayat_id and member.panchayat_id.id or False,
                'image': member.image or False,
                'street': member.street or False,
                'street2': member.street2 or False,
                'phone': member.phone or False,
                'email': member.email or False,
                'mobile': member.mobile or False,
                'zip': member.zip or False,
                'city': member.city or False,
                'country_id':
                member.country_id and member.country_id.id or False,
                'state_id': member.state_id and member.state_id.id or False,
            }

    @api.multi
    def enroll_member(self):
        for record in self:
            total_admission = self.env['op.admission.member'].search_count(
                [('register_id', '=', record.register_id.id),
                 ('state', '=', 'done')])
            if record.register_id.max_count:
                if not total_admission < record.register_id.max_count:
                    msg = 'Max Admission In Admission Register :- (%s)' % (
                        record.register_id.max_count)
                    raise ValidationError(_(msg))
            if not record.member_id:
                vals = record.get_student_vals()
                vals.update({'partner_id': record.partner_id.id})
                member_id = self.env['op.member'].create(vals).id
            else:
                member_id = record.member_id.id
                record.member_id.write({
                    'district_id': record.district_id and record.district_id.id or False,
                    'union_id': record.union_id and record.union_id.id or False,
                    'panchayat_id': record.panchayat_id and record.panchayat_id.id or False,
                })
            record.write({
                'nbr': 1,
                'state': 'done',
                'admission_date': fields.Date.today(),
                'member_id': member_id,
            })

    @api.multi
    def open_member(self):
        form_view = self.env.ref('common_custom_membership.view_op_member_form')
        tree_view = self.env.ref('common_custom_membership.view_op_member_tree')
        value = {
            'domain': str([('id', '=', self.member_id.id)]),
            'view_type': 'form',
            'view_mode': 'tree, form',
            'res_model': 'op.member',
            'view_id': False,
            'views': [(form_view and form_view.id or False, 'form'),
                      (tree_view and tree_view.id or False, 'tree')],
            'type': 'ir.actions.act_window',
            'res_id': self.member_id.id,
            'target': 'current',
            'nodestroy': True
        }
        self.state = 'done'
        return value
