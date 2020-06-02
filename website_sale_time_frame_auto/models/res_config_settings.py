# Copyright 2018 Coop IT Easy SCRLfs
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    send_mail_to_supervisor = fields.Boolean(
        string="Send notification emails to Time frame supervisor",
    )

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        select_type = self.env['ir.config_parameter'].sudo()
        send_mail_to_supervisor = select_type.get_param('website_sale_time_frame_auto.send_mail_to_supervisor')
        res.update({
            'send_mail_to_supervisor': send_mail_to_supervisor
        })
        return res

    @api.multi
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        select_type = self.env['ir.config_parameter'].sudo()
        select_type.set_param('website_sale_time_frame_auto.send_mail_to_supervisor', self.send_mail_to_supervisor)
