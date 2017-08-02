# -*- coding: utf-8 -*-
import logging
from openerp import api, fields, models, _

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    
    _inherit = "sale.order"
    
    raliment_point = fields.Many2one(compute="_compute_raliment", comodel_name="res.partner", string="Raliment Point", domain=[('is_raliment_point','=',True)],store=True)
    time_frame_id = fields.Many2one('time.frame', string="Time Frame")
    
    @api.multi
    @api.depends('partner_id')
    def _compute_raliment(self):
        for order in self:
            if order.partner_id.raliment_point_id and order.partner_id.raliment_point_id:
                order.raliment_point = order.partner_id.raliment_point_id
    
    @api.multi
    def check_customer_credit(self):
        for order in self:
            partner = order.partner_id
            order_total_amount = 0.0
            # This method is used two times : at the validation of the cart and
            # at the payment process. The state of the order is different at these
            # two stages so we need to handle both case. At cart validation we don't
            # have to deduce the order total amount from the amount due.
            if order.state != 'draft':
                order_total_amount = order.amount_total
            #if -(partner.credit - (partner.amount_due - order_total_amount)) >= order.amount_total:
            if partner.customer_credit >= order.amount_total:
                return True
            else:
                return False

class SaleOrderLine(models.Model):
    
    _inherit = "sale.order.line"
    
    raliment_point_id = fields.Many2one(related='order_id.raliment_point', store=True, string='Raliment point')
    time_frame_id = fields.Many2one(related='order_id.time_frame_id', store=True, string="Time Frame")
    
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
    
    uom_name = fields.Char(related="uom_id.name", string="UoM Name")
    supplier_id = fields.Many2one(compute="get_first_supplier", comodel_name="res.partner", string="Supplier") 
    
    invoice_policy = fields.Selection(default='delivery')
    type = fields.Selection(default='product')
    route_ids = fields.Many2many(default=lambda self: self._get_buy_route())
    
    @api.multi
    def get_first_supplier(self):
        for product in self:
            for seller in product.seller_ids:
                product.supplier_id = seller.name
                break

class Partner(models.Model):
    _inherit = "res.partner"
    
    amount_due = fields.Monetary(string="Amount due for sale orders", compute="_compute_amount_due")
    customer_credit = fields.Monetary(string="Customer credit", compute="_compute_customer_credit")
    
    @api.multi
    def _compute_customer_credit(self):
        for partner in self:
            partner.customer_credit = -(partner.credit) - partner.amount_due
            
    @api.multi
    def _compute_amount_due(self):
        order_obj = self.env['sale.order']
        invoice_obj = self.env['account.invoice']
        for partner in self:
            orders = order_obj.search([('partner_id','=',partner.id),('state','in',['sent','sale']),('invoice_status','!=','invoiced')])
            
            amount_total = 0
            for order in orders:
                amount_total += order.amount_total
    
            partner.amount_due = amount_total