import logging
from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class Partner(models.Model):
    _inherit = "res.partner"

    amount_due = fields.Monetary(
        string="Amount due for sale orders",
        compute="_compute_amount_due")
    customer_credit = fields.Monetary(
        string="Customer credit",
        compute="_compute_customer_credit")

    @api.multi
    def _compute_customer_credit(self):
        for partner in self:
            partner.customer_credit = -(partner.credit) - partner.amount_due

    @api.multi
    def _compute_amount_due(self):
        order_obj = self.env['sale.order']

        for partner in self:
            orders = order_obj.search([
                ('partner_id', '=', partner.id),
                ('state', 'in', ['sent', 'sale']),
                ('invoice_status', '!=', 'invoiced')
                ])

            amount_total = 0
            for order in orders:
                amount_total += order.amount_total

            partner.amount_due = amount_total
