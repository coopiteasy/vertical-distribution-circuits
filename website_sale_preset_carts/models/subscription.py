# Copyright 2019 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
#   Houssine Bakkali <houssine@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _
import datetime as dt
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.exceptions import ValidationError


def _parse(date):
    return dt.datetime.strptime(date, DEFAULT_SERVER_DATETIME_FORMAT)


def _format(date):
    return date.strftime(DEFAULT_SERVER_DATETIME_FORMAT)


class Subscription(models.Model):
    _name = 'subscription'
    _description = 'Subscription'

    name = fields.Char(
        required=True)
    active = fields.Boolean(
        string='Active',
        default=True)
    start = fields.Datetime(
        string='Start',
        required=True)
    end = fields.Datetime(
        string='End',
        required=False)
    open_interval = fields.Integer(
        string='Opening Sale Interval',
        default=7,
        help='Specifies how many days before the delivery date '
             'the sale will open for the timeframes')
    close_interval = fields.Integer(
        string='Closing Sale Interval',
        default=2,
        help='Specifies how many days before the delivery date '
             'the sale will open for the timeframes')
    next_delivery = fields.Datetime(
        string='Next Delivery',
        compute='_next_delivery')
    recurring_interval = fields.Integer(
        default=1,
        string='Repeat Every',
        required=True,
        help='Repeat every (Days/Week/Month/Year)')
    recurring_rule = fields.Selection(
        [('daily', 'Day(s)'),
         ('weekly', 'Week(s)')],
        string='Recurrence',
        default='weekly',
        required=True,
        help='Specify Interval for automatic time frame generation.')
    timeframe_ids = fields.One2many(
        comodel_name='time.frame',
        inverse_name='subscription_id',
        string='Time frames')
    subscriber_ids = fields.One2many(
        comodel_name='res.partner',
        inverse_name='subscription_id',
        string='Subscribers')

    def get_relative_delta(self, interval, rule):
        if rule == 'daily':
            return dt.timedelta(days=interval)
        elif rule == 'weekly':
            return dt.timedelta(weeks=interval)

    @api.multi
    def _next_delivery(self):
        for sub in self:
            start = _parse(sub.start)
            today = dt.datetime.today()
            interval = self.get_relative_delta(sub.recurring_interval,
                                               sub.recurring_rule)
            nb_interval = int((today - start) / interval)
            next_delivery = start + nb_interval * interval + interval

            if not sub.end or next_delivery <= _parse(sub.end):
                sub.next_delivery = next_delivery
            else:
                sub.next_delivery = False

    @api.multi
    def create_next_time_frame(self):
        self.ensure_one()
        if not (self.start and self.open_interval and self.close_interval):
            raise ValidationError(_('"Opening Sale Interval" and "Closing '
                                    'Sale Interval" must be set to generate '
                                    'the next timeframe'))
        if self.end and _parse(self.end) <= dt.datetime.today():
            raise ValidationError(_('Subscription ended'))

        start = _parse(self.next_delivery) - dt.timedelta(days=self.open_interval)
        end = _parse(self.next_delivery) - dt.timedelta(days=self.close_interval)
        frame = (
            self.env['time.frame']
            .create({
                    'subscription_id': self.id,
                    'delivery_date': self.next_delivery,
                    'start': _format(start),
                    'end': _format(end),
                    })
        )
        action = {
            'name': _("New Frame"),
            'view_mode': 'form',
            'view_id': False,
            'view_type': 'form',
            'res_model': 'time.frame',
            'res_id': frame.id,
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'current',
            'domain': '[]',
        }
        return action
