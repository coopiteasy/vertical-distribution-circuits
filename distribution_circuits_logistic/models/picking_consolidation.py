# -*- coding: utf-8 -*-
from datetime import datetime

from openerp import api, fields, models, _
import openerp.addons.decimal_precision as dp

class TimeFrameConsolidation(models.Model):
    
    _name = "time.frame.consolidation"
    
    time_frame_id = fields.Many2one('time.frame', readonly=True, required=True)
    delivery_round = fields.Many2one('delivery.round', string="Delivery round", readonly=True)
    picking_consolidations = fields.One2many('picking.consolidation','time_frame_consolidation_id', string="Picking consolidations", readonly=True)
    
class PickingConsolidation(models.Model):
    
    _name = "picking.consolidation"
    
    time_frame_consolidation_id = fields.Many2one('time.frame.consolidation',string='Time frame consolidation', ondelete='cascade', readonly=True)
    time_frame_id = fields.Many2one(related='time_frame_consolidation_id.time_frame_id', readonly=True)
    delivery_address = fields.Many2one('res.partner', string="Delivery address", domain=[('type','=','delivery')], readonly=True)
    consolidation_lines = fields.One2many('picking.consolidation.line','picking_consolidation_id', string='Pickings consolidation')
    
class PickingConsolidationLine(models.Model):
    
    _name = "picking.consolidation.line"
    
    picking_consolidation_id = fields.Many2one('picking.consolidation', string='Picking consolidation')
    product_id = fields.Many2one('product.product', string='Product', required=True, readonly=True)
    product_uom_qty = fields.Float(string='Quantity', digits=dp.get_precision('Product Unit of Measure'), required=True, readonly=True)
    product_uom = fields.Many2one('product.uom', string='Unit of Measure', required=True, readonly=True)
    qty_delivered = fields.Float(string='Delivered', digits=dp.get_precision('Product Unit of Measure'))