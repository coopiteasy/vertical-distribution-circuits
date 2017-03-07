# -*- coding: utf-8 -*-

from openerp import api, fields, models, _

class StockPicking(models.Model):
    
    _inherit = "stock.picking"
    
    raliment_point = fields.Many2one("res.partner", string="Raliment Point", domain=[('is_raliment_point','=',True)])
    
class StockPackOperation(models.Model):
    
    _inherit = "stock.pack.operation"
    
    raliment_point = fields.Many2one(related="picking_id.raliment_point", string="Raliment Point", store=True)