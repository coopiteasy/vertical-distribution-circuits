import logging
from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):

    _inherit = "sale.order"

    time_frame_id = fields.Many2one('time.frame', string="Time Frame")
    raliment_point = fields.Many2one(
        compute="_compute_raliment",
        comodel_name="res.partner",
        string="Raliment Point",
        domain=[('is_raliment_point', '=', True)],
        store=True)
    delivery_point = fields.Many2one(
        compute="_compute_delivery",
        comodel_name="res.partner",
        string="Delivery Point",
        domain=[('is_delivery_point', '=', True)],
        store=True)
    enough_credit = fields.Boolean(
        compute="_compute_enough_credit",
        string="Enough credit")

    @api.multi
    def action_confirm(self):
        for order in self:
            if order.raliment_point:
                order.partner_shipping_id = order.raliment_point
            elif order.delivery_point:
                order.partner_shipping_id = order.delivery_point
        return super(SaleOrder, self).action_confirm()

    @api.multi
    @api.depends('partner_id')
    def _compute_raliment(self):
        for order in self:
            if order.partner_id.raliment_point_id:
                order.raliment_point = order.partner_id.raliment_point_id

    @api.multi
    @api.depends('partner_id')
    def _compute_delivery(self):
        for order in self:
            if order.partner_id.delivery_point_id:
                order.delivery_point = order.partner_id.delivery_point_id

    @api.multi
    def _compute_enough_credit(self):
        for order in self:
            order.enough_credit = order.check_customer_credit()

    @api.multi
    def check_customer_credit(self):
        for order in self:
            partner = order.partner_id
            # This method is used two times : at the validation of the cart and
            # at the payment process. The state of the order is different at
            # these two stages so we need to handle both case.
            # At cart validation we don't have to deduce the order total
            # amount from the amount due.
            if partner.customer_credit >= order.amount_total:
                return True
            else:
                return False


class SaleOrderLine(models.Model):

    _inherit = "sale.order.line"

    raliment_point_id = fields.Many2one(
        related='order_id.raliment_point',
        store=True,
        string='Raliment point')
    time_frame_id = fields.Many2one(
        related='order_id.time_frame_id',
        store=True,
        string="Time Frame")
