# Copyright 2019 Coop IT Easy SCRLfs
#     Houssine Bakkali <houssine@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging
from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model
    def _get_buy_route(self):
        buy_route = self.env.ref('purchase.route_warehouse0_buy')
        mto_route = self.env.ref('stock.route_warehouse0_mto')
        routes_list = []

        if buy_route:
            routes_list.append(buy_route.ids[0])
        if mto_route:
            routes_list.append(mto_route.ids[0])
        return routes_list

    invoice_policy = fields.Selection(default='delivery')
    type = fields.Selection(default='product')
    route_ids = fields.Many2many(default=lambda self: self._get_buy_route())
    uom_name = fields.Char(related="uom_id.name", string="UoM Name")
    supplier_id = fields.Many2one(
        compute="get_first_supplier",
        comodel_name="res.partner",
        string="Supplier")
    supplier_name = fields.Char(related='supplier_id.display_name', string="Supplier Name")

    @api.multi
    def get_first_supplier(self):
        for product in self:
            for seller in product.sudo().seller_ids:
                product.supplier_id = seller.name
                break
