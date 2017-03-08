# -*- coding: utf-8 -*-

from openerp import api, fields, models, _

class DeliveryRound(models.Model):
    _name = "delivery.round"
    
    name = fields.Char(string="Name", required=True)
    time_frame_id = fields.Many2one('time.frame', string='Time frame', required=True)
    delivery_date = fields.Date(related='time_frame_id.delivery_date', store=True)
    lines = fields.One2many('delivery.round.line', 'delivery_round_id', string='Delivery line')
    deliverer = fields.Many2one('res.user', string="Deliverer")
    responsible = fields.Many2one('res.user', string="Responsible")
    
class DeliveryRoundLine(models.Model):    
    _name = "delivery.round.line"
    
    sequence = fields.Integer(string="Sequence")
    delivery_round_id = fields.Many2one('delivery.round', string="Delivery round", required=True)
    raliment_point_id = fields.Many2one('res.partner', string="R'Aliment point", required=True)
    picking_wave = fields.One2many('stock.picking.wave', 'round_line_id', string="Picking wave")
    stock_picking = fields.One2many('stock.picking', 'round_line_id', string="Stock picking")
    