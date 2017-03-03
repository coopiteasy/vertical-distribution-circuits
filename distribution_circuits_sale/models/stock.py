# -*- coding: utf-8 -*-

from openerp import api, fields, models, _

class StockPicking(models.Model):
    
    _inherit = "stock.picking"
    
    raliment_point = fields.Many2one("res.partner", string="Raliment Point", domain=[('is_raliment_point','=',True)])