# -*- coding: utf-8 -*-
from datetime import datetime

from openerp import api, fields, models, _
import openerp.addons.decimal_precision as dp

class TimeFrameConsolidation(models.Model):
    
    _name = "time.frame.consolidation"
    
    time_frame_id = fields.Many2one('time.frame', readonly=True, required=True)
    delivery_round = fields.Many2one('delivery.round', string="Delivery round", readonly=True)
    picking_consolidations = fields.One2many('picking.consolidation','time_frame_consolidation_id', string="Picking consolidations")
    picking_supplier_consolidation = fields.One2many('picking.supplier.consolidation','time_frame_consolidation_id', string="Picking supplier consolidations")
    user_id = fields.Many2one('res.users', string='Responsible', default=lambda self: self.env.user)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env['res.company']._company_default_get('sale.order'))
    
class PickingConsolidation(models.Model):
    
    _name = "picking.consolidation"
    
    time_frame_consolidation_id = fields.Many2one('time.frame.consolidation',string='Time frame consolidation', ondelete='cascade', readonly=True)
    time_frame_id = fields.Many2one(related='time_frame_consolidation_id.time_frame_id', readonly=True)
    delivery_address = fields.Many2one('res.partner', string="Delivery address", domain=[('is_delivery_point','=',True)], readonly=True)
    consolidation_lines = fields.One2many('picking.consolidation.line','picking_consolidation_id', string='Pickings consolidation')    
    
class PickingConsolidationLine(models.Model):
    
    _name = "picking.consolidation.line"
    _order = "supplier,product_id"
    
    picking_consolidation_id = fields.Many2one('picking.consolidation', string='Picking consolidation')
    product_id = fields.Many2one('product.product', string='Product', required=True, readonly=True)
    supplier = fields.Char(compute='_get_supplier_name', store=True)
    product_uom_qty = fields.Float(string='Quantity', digits=dp.get_precision('Product Unit of Measure'), required=True, readonly=True)
    product_uom = fields.Many2one('product.uom', string='Unit of Measure', required=True, readonly=True)
    qty_delivered = fields.Float(string='Delivered', digits=dp.get_precision('Product Unit of Measure'))
    
    @api.multi
    @api.depends('product_id')
    def _get_supplier_name(self):
        for line in self:
            line.supplier = line.product_id.product_tmpl_id.supplier_id.display_name

class PickingSupplierConsolidation(models.Model):
    
    _name = "picking.supplier.consolidation"
    
    time_frame_consolidation_id = fields.Many2one('time.frame.consolidation',string='Time frame consolidation', ondelete='cascade', readonly=True)
    time_frame_id = fields.Many2one(related='time_frame_consolidation_id.time_frame_id', readonly=True)
    supplier = fields.Many2one('res.partner', string="Supplier", readonly=True)
    supplier_consolidation_lines = fields.One2many('supplier.consolidation.line','supplier_consolidation_id', string='Pickings consolidation')

class PickingConsolidationLine(models.Model):
    
    _name = "supplier.consolidation.line"
    _order = "product_id,raliment_point_id"
    
    supplier_consolidation_id = fields.Many2one('picking.supplier.consolidation', string='Picking supplier consolidation')
    raliment_point_id = fields.Many2one('res.partner', string="Raliment point", readonly=True)
    product_id = fields.Many2one('product.product', string='Product', required=True, readonly=True)
    product_uom_qty = fields.Float(string='Quantity', digits=dp.get_precision('Product Unit of Measure'), required=True, readonly=True)
    product_uom = fields.Many2one('product.uom', string='Unit of Measure', required=True, readonly=True)
