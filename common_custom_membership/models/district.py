import datetime
from odoo import models, fields, api, _
import logging
from odoo.exceptions import ValidationError


class District(models.Model):
    _name = "op.district"
    _rec_name = 'district_name'

    district_name = fields.Char('District Name', size=256, required=True)
    district_code = fields.Char('Code', size=256, required=True)
    union_ids = fields.One2many('op.union','district_id',string='Union(s)')

    _sql_constraints = [
        ('unique_district_name',
         'unique(district_name)', 'District Name already exists!')]

    @api.multi
    @api.constrains('district_name')
    def _check_district_name(self):
        for record in self:
            list_ids = record.search([('id','!=',record.id)])
            logging.info(list_ids)
            for id in list_ids:
                logging.info(self.district_name)
                logging.info(id.district_name)
                if self.district_name.lower() == id.district_name.lower():
                    raise ValidationError(_("District Name already exists!"))
