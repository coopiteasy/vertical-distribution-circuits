# Copyright 2018 Coop IT Easy SCRLfs
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from ast import literal_eval

from odoo import api, models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    cart_abandoned_before_timeframe_end_delay = fields.Float(
        "Delay Before End of Time Frame",
        default=24.0,
        help="Number of hours before the end of the time frame when a "
             "reminder is sent",
    )

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        param_mgr = self.env['ir.config_parameter']

        cart_delay = float(
            param_mgr.sudo().get_param(
                'distribution_circuits_sale'
                '.cart_abandoned_before_timeframe_end_delay',
                default='24.0'
            )
        )

        res.update(
            cart_abandoned_before_timeframe_end_delay=cart_delay,
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        param_mgr = self.env['ir.config_parameter']
        param_mgr.sudo().set_param(
            'distribution_circuits_sale'
            '.cart_abandoned_before_timeframe_end_delay',
            self.cart_abandoned_before_timeframe_end_delay
        )
