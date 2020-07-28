# Copyright 2019 Coop IT Easy SCRLfs
#     Robin Keunen <robin@coopiteasy.be>
#     Houssine Bakkali <houssine@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models, _
from odoo.exceptions import UserError
# from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as _format
import pytz
import logging


_logger = logging.getLogger(__name__)


class TimeFrame(models.Model):
    _inherit = 'time.frame'

    preset_cart_id = fields.Many2one(
        comodel_name='preset.cart',
        string='Preset Cart')

    preset_cart_line_ids = fields.One2many(
        comodel_name='preset.cart.line',
        related='preset_cart_id.cart_line_ids',
    )
    subscription_id = fields.Many2one(
        comodel_name='subscription',
        string='Subscription',
        required=False)
    subscriber_ids = fields.One2many(
        related='subscription_id.subscriber_ids',
        string='Subscribers')
    block_insufficient_credit = fields.Boolean(
        string='Block orders with insufficient credit')
    blocked_order_ids = fields.One2many(
        comodel_name='time.frame.blocked.order',
        inverse_name='time_frame_id',
        string="Blocked orders")

    @api.model
    def localize(self, d):
        tz_name = self.env['res.users'].browse(1).tz
        tz_name = tz_name if tz_name else 'UTC'

        if not d.tzinfo:
            utc_tz = pytz.timezone('UTC')
            d = utc_tz.localize(d)

        context_tz = pytz.timezone(tz_name)
        return d.astimezone(context_tz)

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
            if self.env['ir.config_parameter'].sudo().get_param(
                    'website_sale_preset_carts.send_sale_order_on_timeframe_open'
            ):
                order.force_quotation_send()
            order.state = 'draft'
        return super(TimeFrame, self).action_open()

    @api.multi
    def action_close(self):
        self.ensure_one()
        for order in self.sale_orders:
            if order.state == 'draft':
                if order.partner_id.is_subscribed(self.delivery_date):
                    if self.env['ir.config_parameter'].sudo().get_param(
                        'website_sale_preset_carts.'
                        'send_sale_order_on_timeframe_close'
                    ):
                        order.with_context(send_email=True).action_confirm()
                    else:
                        order.with_context(send_email=False).action_confirm()
                    order.action_done()
        return super(TimeFrame, self).action_close()

    def _prepare_order_lines(self):
        # fixme : seems that list price on customer won't be taken into account
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
            so_line = self.env['sale.order.line'].create(line)
            so_line.product_id_change()
        return sale_order

    def compute_cart_amount(self, subscriber, lines):
        amount = [line['price_unit'] * line['product_uom_qty'] *
                  subscriber.nb_household for line in lines][0]
        return amount

    @api.model
    def generate_sale_orders(self):
        blocked_order_obj = self.env['time.frame.blocked.order']

        for frame in self:

            unit_lines = frame._prepare_order_lines()

            # we first get the customers with the corresponding subscription
            customers = (
                self.env['res.partner']
                    .search([
                        ('subscription_id', '!=', False),
                        ('subscription_id', '=', frame.subscription_id.id)
                        ])
            )

            # we then filter based on suspended date if suspended
            subscribers = customers.filtered(
                lambda cust: cust.is_subscribed(frame.delivery_date)
            )

            for subscriber in subscribers:
                cart_amount = self.compute_cart_amount(subscriber, unit_lines)
                if not frame.block_insufficient_credit or cart_amount <= subscriber.customer_credit:
                    order = self._create_sale_order(subscriber, unit_lines)
                    frame.sale_orders += order
                    subscriber.write({'last_website_so_id': order.id})
                else:
                    blocked_order_obj.create({
                        'partner_id': subscriber.id,
                        'time_frame_id': frame.id,
                        'necessary_amount': cart_amount,
                        'customer_credit': subscriber.customer_credit})


class TimeFrameBlockedOrder(models.Model):
    _name = "time.frame.blocked.order"

    time_frame_id = fields.Many2one(
        comodel_name='time.frame',
        string="Time frame")
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string="Subscriber")
    customer_credit = fields.Monetary(
        string="Customer credit")
    necessary_amount = fields.Monetary(
        string="Necessary amount")
    state = fields.Selection(
        [('insufficient', 'Insufficient credit'),
         ('manual', 'Forced validation')],
        string="State",
        default='insufficient')
    validated_by = fields.Many2one(
        comodel_name='res.users',
        string="Validated by",
        readonly=True)
    sale_order = fields.Many2one(
        comodel_name='sale.order',
        string="Sale order",
        readonly=True)
    currency_id = fields.Many2one(
        related='company_id.currency_id',
        string="Company Currency",
        readonly=True)
    company_id = fields.Many2one(
        related="time_frame_id.company_id")

    @api.multi
    def action_validation(self):
        self.ensure_one()
        frame = self.time_frame_id
        if frame.state == 'open':
            unit_lines = frame._prepare_order_lines()
            order = frame._create_sale_order(self.partner_id, unit_lines)
            frame.sale_orders += order
            self.partner_id.write({'last_website_so_id': order.id})
            self.state = 'manual'
        else:
            raise UserError(_("You cannot validate manually a blocked order "
                              "if the time frame is not open anymore."))
