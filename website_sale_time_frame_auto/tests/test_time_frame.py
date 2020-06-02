# Copyright 2019 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
#   Manuel Claeys Bouuaert <manuel@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase
import datetime as dt
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF


class TestTimeFrame(TransactionCase):

    def test_starting_validated_frames_are_opened(self):
        frame = self.env.ref('distribution_circuits_sale.demo_timeframe_future')
        frame.start = dt.datetime.now() - dt.timedelta(minutes=45)
        frame.end = dt.datetime.now() - dt.timedelta(minutes=15)

        frame.action_validate()
        self.assertEqual(frame.state, 'validated')
        self.env['time.frame'].open_timeframes()
        self.assertEqual(frame.state, 'open')

    def test_closing_opened_frames_are_closed(self):
        frame = self.env.ref('distribution_circuits_sale.demo_timeframe_future')
        frame.start = dt.datetime.now() - dt.timedelta(minutes=45)
        frame.end = dt.datetime.now() - dt.timedelta(minutes=15)

        frame.action_validate()
        frame.action_open()
        self.assertEqual(frame.state, 'open')
        self.env['time.frame'].close_timeframes()
        self.assertEqual(frame.state, 'closed')
