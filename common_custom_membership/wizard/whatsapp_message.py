from odoo import models, api, fields


class SendMessage(models.TransientModel):

    _name = 'op.whatsapp.message.wizard'

    message = fields.Text(string="Message", required=True)

    def send_message(self):
        if self.message:
            return {
                'type': 'ir.actions.act_url',
                'url': "https://web.whatsapp.com/send?phone=" + "&text=" + self.message,
                'target': 'new',
                'res_id': self.id,
            }