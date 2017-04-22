# -*- coding: utf-8 -*-

from openerp import api, fields, models, _

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

class Product(models.Model):
    
    _inherit = "product.template"
    
    uom_name = fields.Char(related="uom_id.name", string="UoM Name")
    supplier_id = fields.Many2one(compute="get_first_supplier", comodel_name="res.partner", string="Supplier") 
    
    @api.multi
    def get_first_supplier(self):
        for seller in self.seller_ids:
            self.supplier_id = seller.name
            break

class Partner(models.Model):
    _inherit = "res.partner"
    
    amount_due = fields.Monetary(string="Amount due", compute="_compute_amount_due")
    
    @api.multi
    def _compute_amount_due(self):
        order_obj = self.env['sale.order']
        invoice_obj = self.env['account.invoice']
        for partner in self:
            orders = order_obj.search([('partner_id','=',partner.id),('state','in',['sent','sale','done']),('invoice_status','!=','invoiced')])
            invoices = invoice_obj.search([('partner_id','=',partner.id),('state','=','open')])
            invoices_child = invoice_obj.search([('partner_id','in',partner.child_ids.ids),('state','=','open')])
            invoices |= invoices_child
            
            amount_total = 0
            for order in orders:
                amount_total += order.amount_total
            for invoice in invoices:
                amount_total += invoice.residual
    
            partner.amount_due = amount_total