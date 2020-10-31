from odoo import models, api, fields,_
import smtplib
import logging
from odoo.exceptions import UserError, ValidationError
# import webbrowser
# from time import sleep


class OpLanguageWizard(models.Model):
    _name = 'op.language.wizard'

    @api.model
    def _default_language(self):
        if self._context.get('active_model') == 'res.lang':
            lang = self.env['res.lang'].browse(self._context.get('active_id'))
            return lang.code
        return False

    @api.model
    def _get_languages(self):
        return self.env['res.lang'].get_installed()

    lang = fields.Selection(_get_languages, string='Language', required=True,
                            default=_default_language)
    overwrite = fields.Boolean('Overwrite Existing Terms',default=True,
                               help="If you check this box, your customized translations will be overwritten and replaced by the official ones.")
    state = fields.Selection([('init', 'init'), ('done', 'done')],
                             string='Status', readonly=True, default='init')

    @api.multi
    def lang_install(self):
        self.ensure_one()
        mods = self.env['ir.module.module'].search([('state', '=', 'installed')])
        mods.with_context(overwrite=self.overwrite)._update_translations(self.lang)
        self.state = 'done'
        user = self.env['res.users'].search([('id','=',self.env.uid)])
        user.write({'lang':self.lang})
        return {
            'name': _('Language Pack'),
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': False,
            'res_model': 'op.language.wizard',
            'domain': [],
            'context': dict(self._context, active_ids=self.ids),
            'type': 'ir.actions.act_window',
            'target': 'new',
            'res_id': self.id,
        }

    def reload(self):
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

        # url = input('Input the URL to reload, including "http://localhost:8069/web?debug=1#id=&view_type=form&model=op.registration.wizard&action=127" ')

        # while True:
        #     print("refreshing...")
        #     webbrowser.open(url, new=0)
        #     sleep(10)
