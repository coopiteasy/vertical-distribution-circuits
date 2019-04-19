import logging
from odoo import api, models

_logger = logging.getLogger(__name__)


class ProcurementRule(models.Model):

    _inherit = 'procurement.rule'

    def get_time_frame_origin(self, origin):
        sale_order = self.env['sale.order'].search([('name', '=', origin)])
        return sale_order.time_frame_id

    def _prepare_purchase_order(self, product_id, product_qty, product_uom, origin, values, partner):
        values = super(ProcurementRule, self)._prepare_purchase_order(product_id, product_qty, product_uom, origin, values, partner)

        time_frame = self.get_time_frame_origin(origin)
        if time_frame:
            values['time_frame_id'] = time_frame.id
        return values

    def _make_po_get_domain(self, values, partner):
        domain = super(ProcurementRule, self)._make_po_get_domain(values,
                                                                  partner)
        time_frame = self.get_time_frame_origin(values['origin'])
        if time_frame:
            domain += (('time_frame_id', '=', time_frame.id),)
        return domain

    @api.multi
    def _run_buy(self, product_id, product_qty, product_uom, location_id, name,
                 origin,
                 values):
        values['origin'] = origin
        super(ProcurementRule, self)._run_buy(product_id, product_qty,
                                              product_uom,
                                              location_id,
                                              name,
                                              origin, values)
