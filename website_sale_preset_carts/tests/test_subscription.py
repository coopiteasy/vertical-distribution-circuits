# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase
import datetime as dt
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


def _format(date):
    return date.strftime(DEFAULT_SERVER_DATETIME_FORMAT)


class TestSubscription(TransactionCase):
    def test_subscription_next_delivery(self):
        Subscription = self.env['subscription']
        today = dt.datetime.today()
        sub1 = Subscription.create({
            'name': 'sub-test-1',
            'start': today - dt.timedelta(weeks=3, days=2),
            'recurring_interval': 1,
            'recurring_rule': 'weekly',
        })
        next = _format(today + dt.timedelta(days=5))
        self.assertEqual(next, sub1.next_delivery)

        sub2 = Subscription.create({
            'name': 'sub-test-2',
            'start': today - dt.timedelta(weeks=4, days=4),
            'recurring_interval': 2,
            'recurring_rule': 'weekly',
        })
        next = _format(today + dt.timedelta(weeks=1, days=3))
        self.assertEqual(next, sub2.next_delivery)

        sub3 = Subscription.create({
            'name': 'sub-test-3',
            'start': '2018-05-28',
            'end': '2019-05-28',
            'recurring_interval': 1,
            'recurring_rule': 'weekly',
        })
        self.assertFalse(sub3.next_delivery)

    def test_create_next_time_frame(self):
        Subscription = self.env['subscription']
        sub = Subscription.create({
            'name': 'sub-test-3',
            'start': '2018-05-28',
            'recurring_interval': 1,
            'recurring_rule': 'weekly',
        })
        action = sub.create_next_time_frame()
        # from pprint import pprint
        # pprint(action)
        self.assertTrue(True)
