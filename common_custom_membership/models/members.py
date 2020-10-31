from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class OpMember(models.Model):
    _name = 'op.member'
    _inherits = {'res.partner': 'partner_id'}

    middle_name = fields.Char('Middle Name', size=128)
    last_name = fields.Char('Last Name', size=128)
    birth_date = fields.Date('Birth Date')
    blood_group = fields.Selection(
        [('A+', 'A+ve'), ('B+', 'B+ve'), ('O+', 'O+ve'), ('AB+', 'AB+ve'),
         ('A-', 'A-ve'), ('B-', 'B-ve'), ('O-', 'O-ve'), ('AB-', 'AB-ve')],
        'Blood Group')
    gender = fields.Selection(
        [('m', 'Male'), ('f', 'Female'),
         ('o', 'Other')], 'Gender')
    nationality = fields.Many2one('res.country', 'Nationality')
    emergency_contact = fields.Many2one(
        'res.partner', 'Emergency Contact')
    already_partner = fields.Boolean('Already Partner')
    partner_id = fields.Many2one(
        'res.partner', 'Partner', required=True, ondelete="cascade")
    district_id = fields.Many2one('op.district', 'District')
    union_id = fields.Many2one('op.union', 'Union')
    panchayat_id = fields.Many2one('op.panchayat', 'Panchayat')

    @api.multi
    @api.constrains('birth_date')
    def _check_birthdate(self):
        for record in self:
            if record.birth_date > fields.Date.today():
                raise ValidationError(_(
                    "Birth Date can't be greater than current date!"))


class ResUsers(models.Model):
    _inherit = "res.users"

    user_line = fields.One2many('op.member', 'user_id', 'User Line')
    child_ids = fields.Many2many(
        'res.users', 'res_user_first_rel1',
        'user_id', 'res_user_second_rel1', string='Childs')

    @api.multi
    def create_user(self, records, user_group=None):
        for rec in records:
            if not rec.user_id:
                user_vals = {
                    'name': rec.name,
                    'login': rec.email or (rec.name + rec.last_name),
                    'partner_id': rec.partner_id.id,
                    'email': rec.email,
                    'password': rec.name + '@123'
                }
                user_id = self.create(user_vals)
                rec.user_id = user_id
                if user_group:
                    user_group.users = user_group.users + user_id
