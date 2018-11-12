# Copyright 2018 Coop IT Easy SCRLfs
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import datetime

from ast import literal_eval

from odoo import api, models, fields
from odoo.osv import expression


class SaleOrder(models.Model):
    _inherit = "sale.order"

    is_abandoned_cart_near_timeframe_end = fields.Boolean(
        'Is Abandoned Cart Near Timeframe End',
        compute='_compute_abandoned_cart_near_timeframe_end',
        search='_search_abandoned_cart_near_timeframe_end',
    )
    cart_reminder_email_before_timeframe_end_sent = fields.Boolean(
        'Cart reminder email before timeframe end already sent'
    )

    @api.multi
    @api.depends('team_id.team_type', 'date_order', 'order_line',
                 'state', 'partner_id')
    def _compute_abandoned_cart_near_timeframe_end(self):
        delay = float(
            self.env['ir.config_parameter'].sudo()
            .get_param('distribution_circuits_sale'
                       '.cart_abandoned_before_timeframe_end_delay')
        )
        timeframe_end = fields.Datetime.to_string(
            datetime.datetime.utcnow() + datetime.timedelta(hours=delay)
        )
        for order in self:
            order.is_abandoned_cart_near_timeframe_end = bool(
                order.time_frame_id.end <= timeframe_end
                and order.is_abandoned_cart
            )

    def _search_abandoned_cart_near_timeframe_end(self, operator, value):
        delay = float(
            self.env['ir.config_parameter'].sudo()
            .get_param('distribution_circuits_sale'
                       '.cart_abandoned_before_timeframe_end_delay')
        )
        timeframe_end = fields.Datetime.to_string(
            datetime.datetime.utcnow() + datetime.timedelta(hours=delay)
        )
        domain = expression.normalize_domain([
            ('time_frame_id.end', '<=', timeframe_end),
            ('is_abandoned_cart', operator, bool(value)),
        ])
        return domain

    @api.model
    def _cron_send_mail_before_timeframe_end(self):
        mail_mgr = self.env['mail.template']
        orders = self.env['sale.order'].search([
            ('is_abandoned_cart_near_timeframe_end', '=', True)
        ])
        mail_template = self.env.ref(
            'distribution_circuits_sale'
            '.cart_reminder_mail_before_timeframe_end'
        )
        for order in orders:
            order.cart_reminder_email_before_timeframe_end_sent = (
                mail_mgr.browse(mail_template.id).send(order.id)
            )
        return True
