# -*- coding: utf-8 -*-

from openerp import api, fields, models, _

class StockPicking(models.Model):
    
    _inherit = "stock.picking"
    
    time_frame_id = fields.Many2one(compute="_compute_time_frame", comodel_name="time.frame", string="Time Frame", store=True)
    raliment_point = fields.Many2one(compute="_compute_partners", comodel_name="res.partner", string="Raliment Point", domain=[('is_raliment_point','=',True)],store=True)
    delivery_address = fields.Many2one(compute="_compute_partners", comodel_name="res.partner", string="Delivery address", store=True)
    #round_line_id = fields.Many2one("delivery.round.line", string="Delivery round line")
    partner_id = fields.Many2one(compute="_compute_partners", comodel_name="res.partner", string='Partner', states={'done': [('readonly', True)], 'cancel': [('readonly', True)]})
    
    @api.multi
    @api.depends('move_lines')
    def _compute_partners(self):
        for picking in self: 
            if picking.sale_id:
                picking.raliment_point = picking.sale_id.raliment_point
                picking.partner_id = picking.sale_id.partner_id
                picking.delivery_address = picking.sale_id.partner_shipping_id

    @api.multi
    @api.depends('move_lines')
    def _compute_time_frame(self):
        for picking in self:    
            if picking.sale_id:
                picking.time_frame_id = picking.sale_id.time_frame_id
            
class StockPickingWave(models.Model):
    
    _inherit = "stock.picking.wave"
    
    round_line = fields.One2many("delivery.round.line", "picking_wave", string="Delivery round line")
        
class StockPackOperation(models.Model):
    
    _inherit = "stock.pack.operation"
    
    raliment_point = fields.Many2one(related="picking_id.raliment_point", string="Raliment Point", store=True)
    delivery_address = fields.Many2one(related="picking_id.delivery_address", string="Delivery Address", store=True)