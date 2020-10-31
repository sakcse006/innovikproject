import datetime
from odoo import models, fields, api, _
import logging
from odoo.exceptions import ValidationError


class Union(models.Model):
    _name = "op.union"
    _rec_name = 'union_name'

    union_name = fields.Char('Union Name', size=128, required=True)
    union_code = fields.Char('Code', size=256, required=True)
    district_id = fields.Many2one('op.district', 'District', required=True)
    panchayat_ids = fields.One2many('op.panchayat', 'union_id', string='Panchayat(s)')

    _sql_constraints = [
        ('unique_union_name',
         'unique(union_name)', 'Union Name already exists!')]

    @api.multi
    @api.constrains('union_name')
    def _check_union_name(self):
        for record in self:
            list_ids = record.search([('id','!=',record.id)])
            logging.info(list_ids)
            for id in list_ids:
                logging.info(self.union_name)
                logging.info(id.union_name)
                if self.union_name.lower() == id.union_name.lower():
                    raise ValidationError(_("Union Name already exists!"))
