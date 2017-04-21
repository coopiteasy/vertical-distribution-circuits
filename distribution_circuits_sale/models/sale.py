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