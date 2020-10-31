import datetime
from odoo import models, fields, api, _
import logging
from odoo.exceptions import ValidationError


class Panchayat(models.Model):
    _name = "op.panchayat"
    _rec_name = 'panchayat_name'

    panchayat_name = fields.Char('Panchayat Name', size=128, required=True)
    panchayat_code = fields.Char('Code', size=256, required=True)
    union_id = fields.Many2one('op.union', 'Union', required=True)

    _sql_constraints = [
        ('unique_panchayat_name',
         'unique(panchayat_name)', 'Panchayat Name already exists!')]

    @api.multi
    @api.constrains('panchayat_name')
    def _check_panchayat_name(self):
        for record in self:
            list_ids = record.search([('id','!=',record.id)])
            logging.info(list_ids)
            for id in list_ids:
                logging.info(self.panchayat_name)
                logging.info(id.panchayat_name)
                if self.panchayat_name.lower() == id.panchayat_name.lower():
                    raise ValidationError(_("Panchayat Name already exists!"))
