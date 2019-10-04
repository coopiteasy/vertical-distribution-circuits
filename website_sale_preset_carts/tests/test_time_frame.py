# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase
import datetime as dt
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF


class TestTimeFrame(TransactionCase):

    def test_generate_sale_orders_based_on_cart_lines(self):
        partner1 = self.env.ref(
            'distribution_circuits_base.partner_raliment_customer_1')
        partner3 = self.env.ref(
            'distribution_circuits_base.partner_raliment_customer_3')
        frame = self.env.ref(
            'distribution_circuits_sale.demo_timeframe_future')
        frame.generate_sale_orders()

        generated_so = self.env['sale.order'].search([
            ('origin', '=', frame.name),
              ]
        )

        self.assertTrue(partner1.id in generated_so.mapped('partner_id.id'))
        self.assertFalse(partner3.id in generated_so.mapped('partner_id.id'))

        for order in generated_so:
            order_lines = sorted([
                (ol.id, ol.product_uom_qty) for ol in order.order_line
            ])
            cart_lines = sorted([
                (l.id, l.quantity) for l in frame.preset_cart_id.cart_line_ids
            ])

            self.assertEqual(len(cart_lines), len(order_lines))
            self.assertItemsEqual(
                [round(q * order.partner_id.nb_household, 2) for i, q in cart_lines],
                [round(q, 2) for i, q in order_lines],
            )

    def test_action_open_generates_sale_orders(self):
        frame = self.env.ref('distribution_circuits_sale.demo_timeframe_future')
        frame.action_validate()
        frame.action_open()

        self.assertEqual(frame.state, 'open')
        self.assertTrue(all(
            (s == 'draft' for s in frame.sale_orders.mapped('state'))
        ))

    def test_starting_validated_frames_are_opened(self):
        frame = self.env.ref('distribution_circuits_sale.demo_timeframe_future')
        frame.start = dt.datetime.now() - dt.timedelta(minutes=45)
        frame.end = dt.datetime.now() - dt.timedelta(minutes=15)

        frame.action_validate()
        self.assertEqual(frame.state, 'validated')

        self.env['time.frame'].open_timeframes()
        self.assertEqual(frame.state, 'open')

        self.assertTrue(frame.sale_orders)
        self.assertEqual(len(frame.sale_orders), 1)
        self.assertTrue(all((o.state == 'draft' for o in frame.sale_orders)))

    def test_closing_opened_frames_are_closed(self):
        frame = self.env.ref('distribution_circuits_sale.demo_timeframe_future')
        frame.start = dt.datetime.now() - dt.timedelta(minutes=45)
        frame.end = dt.datetime.now() - dt.timedelta(minutes=15)

        frame.action_validate()
        frame.action_open()

        self.assertEqual(frame.state, 'open')
        self.env['time.frame'].close_timeframes()
        self.assertEqual(frame.state, 'closed')
        self.assertTrue(frame.sale_orders)
        self.assertTrue(all((o.state == 'done' for o in frame.sale_orders)))

    def test_timeframe_nosubscription(self):
        frame = self.env.ref('website_sale_preset_carts.demo_timeframe_current_nosubscription')
        frame.action_validate()
        frame.action_open()
        self.assertFalse(frame.sale_orders)


    def test_partner_is_subscribed(self):
        partner1 = self.env.ref(
            'distribution_circuits_base.partner_raliment_customer_1')
        partner2 = self.env.ref(
            'distribution_circuits_base.partner_raliment_customer_2')
        partner3 = self.env.ref(
            'distribution_circuits_base.partner_raliment_customer_3')
        partner3.subscription_id = False

        future_date = (
                dt.date.today() + dt.timedelta(days=60)
        ).strftime(DTF)

        self.assertTrue(partner1.is_subscribed())
        self.assertTrue(partner1.is_subscribed(future_date))

        self.assertTrue(partner2.is_subscribed())
        self.assertFalse(partner2.is_subscribed(future_date))

        self.assertFalse(partner3.is_subscribed())
        self.assertFalse(partner3.is_subscribed(future_date))
