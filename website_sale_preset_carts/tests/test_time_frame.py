# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestTimeFrame(TransactionCase):

    def test_generate_sale_orders_based_on_cart_lines(self):
        # fixme useful name and cases
        partner1 = self.env.ref('distribution_circuits_base.partner_raliment_customer_1')  # noqa
        partner2 = self.env.ref('distribution_circuits_base.partner_raliment_customer_3')  # noqa
        frame = self.env.ref('distribution_circuits_sale.demo_timeframe_current')
        frame.generate_sale_orders()

        generated_so = self.env['sale.order'].search([
            ('origin', '=', frame.name),
              ]
        )

        self.assertTrue(partner1.id in generated_so.mapped('partner_id.id'))
        self.assertTrue(partner2.id in generated_so.mapped('partner_id.id'))

        for order in generated_so:
            order_lines = sorted([
                (ol.id, ol.product_uom_qty) for ol in order.order_line
            ])
            cart_lines = sorted([
                (l.id, l.quantity) for l in frame.preset_cart_id.cart_line_ids
            ])

            self.assertEqual(len(cart_lines), len(order_lines))
            self.assertItemsEqual(
                [q * order.partner_id.nb_household for i, q in cart_lines],
                [q for i, q in order_lines],
            )

    def test_action_open_generates_sale_orders(self):
        frame = self.env.ref('distribution_circuits_sale.demo_timeframe_future')
        frame.action_validate()
        frame.action_open()

        self.assertEqual(frame.state, 'open')
        self.assertTrue(all(
            (s == 'draft' for s in frame.sale_orders.mapped('state'))
        ))
