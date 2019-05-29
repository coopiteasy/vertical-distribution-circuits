# Copyright 2019 Coop IT Easy SCRLfs
#     Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class TimeFrame(models.Model):
    _inherit = 'time.frame'

    preset_cart_id = fields.Many2one(
        comodel_name='preset.cart',
        string='Preset Cart')

    preset_cart_line_ids = fields.One2many(
        comodel_name='preset.cart.line',
        related='preset_cart_id.cart_line_ids',
    )

    @api.multi
    def action_open(self):
        self.ensure_one()
        self.generate_sale_orders()
        return super(TimeFrame, self).action_open()

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

