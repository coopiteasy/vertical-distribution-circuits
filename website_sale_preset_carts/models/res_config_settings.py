# Copyright 2018 Coop IT Easy SCRLfs
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    send_sale_order_on_timeframe_open = fields.Boolean(
        string="Email when Timeframe is Opened",
    )
    send_sale_order_on_timeframe_close = fields.Boolean(
        string="Email when Timeframe is Closed",
    )
    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        select_type = self.env['ir.config_parameter'].sudo()
        send_sale_order_on_timeframe_open = select_type.get_param('website_sale_preset_carts.send_sale_order_on_timeframe_open')
        send_sale_order_on_timeframe_close = select_type.get_param('website_sale_preset_carts.send_sale_order_on_timeframe_close')
        res.update({
            'send_sale_order_on_timeframe_open': send_sale_order_on_timeframe_open,
            'send_sale_order_on_timeframe_close': send_sale_order_on_timeframe_close,
        })
        return res

    @api.multi
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        select_type = self.env['ir.config_parameter'].sudo()
        select_type.set_param('website_sale_preset_carts.send_sale_order_on_timeframe_open', self.send_sale_order_on_timeframe_open)
        select_type.set_param('website_sale_preset_carts.send_sale_order_on_timeframe_close', self.send_sale_order_on_timeframe_close)
