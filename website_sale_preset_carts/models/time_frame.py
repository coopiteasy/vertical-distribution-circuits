# Copyright 2019 Coop IT Easy SCRLfs
#     Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models
from datetime import datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as _format


class TimeFrame(models.Model):
    _inherit = 'time.frame'

    preset_cart_id = fields.Many2one(
        comodel_name='preset.cart',
        string='Preset Cart')

    preset_cart_line_ids = fields.One2many(
        comodel_name='preset.cart.line',
        related='preset_cart_id.cart_line_ids',
    )

    @api.model
    def open_timeframes(self):
        now = datetime.now().replace(minute=0, second=0)
        last_hour = now - timedelta(hours=1)
        frames = self.search([
            ('state', '=', 'validated'),
            ('start', '>=', last_hour.strftime(_format)),
            ('start', '<=', now.strftime(_format)),
        ])
        for frame in frames:
            frame.action_open()

    @api.model
    def close_timeframes(self):
        now = datetime.now().replace(minute=0, second=0)
        last_hour = now + timedelta(hours=1)

        frames = self.search([
            ('state', '=', 'open'),
            ('end', '>=', last_hour.strftime(_format)),
            ('end', '<=', now.strftime(_format)),
        ])
        for frame in frames:
            frame.action_close()

    @api.multi
    def action_draft(self):
        self.ensure_one()
        self.sale_orders.action_cancel()
        return super(TimeFrame, self).action_draft()

    @api.multi
    def action_open(self):
        self.ensure_one()
        self.generate_sale_orders()
        for order in self.sale_orders.filtered(lambda so: so.state == 'draft'):
            order.force_quotation_send()
            order.state = 'draft'
        return super(TimeFrame, self).action_open()

    @api.multi
    def action_close(self):
        self.ensure_one()

        for order in self.sale_orders:
            if order.state == 'draft':
                if order.partner_id.is_subscribed(self.delivery_date):
                    # should I prevent sending email?
                    order.action_confirm()
                    order.action_done()

        return super(TimeFrame, self).action_close()

    def _prepare_order_lines(self):

        lines = []
        for cart_line in self.preset_cart_id.cart_line_ids:
            lines.append({
                'name': cart_line.product_id.name,
                'product_id': cart_line.product_id.id,
                'product_uom_qty': cart_line.quantity,
                'product_uom': cart_line.uom_id.id,
                'price_unit': cart_line.product_id.list_price,
            })
        return lines

    def _create_sale_order(self, customer, lines):

        def adapt_qty_for_household(line):
            line = line.copy()
            line['product_uom_qty'] = (
                    line['product_uom_qty'] * customer.nb_household
            )
            return line

        lines = [adapt_qty_for_household(line) for line in lines]

        sale_order = self.env['sale.order'].create({
            'partner_id': customer.id,
            'partner_invoice_id': customer.id,
            'partner_shipping_id': customer.id,
            'origin': self.name,
        })
        for line in lines:
            line['order_id'] = sale_order.id
            self.env['sale.order.line'].create(line)
        return sale_order

    @api.model
    def generate_sale_orders(self):
        for frame in self:

            unit_lines = frame._prepare_order_lines()

            customers = (
                self.env['res.partner']
                    .search([('cart_subscription', '=', True),
                             '|', ('cart_suspended_date', '=', False),
                                  ('cart_suspended_date', '<=', frame.delivery_date)])
            )

            for customer in customers:
                order = self._create_sale_order(customer, unit_lines)
                frame.sale_orders += order
                customer.write({'last_website_so_id': order.id})
