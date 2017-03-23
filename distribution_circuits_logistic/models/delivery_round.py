# -*- coding: utf-8 -*-

from openerp import api, fields, models, _

class DeliveryRound(models.Model):
    _name = "delivery.round"
    
    name = fields.Char(string="Name", required=True, defailt="/")
    time_frame_id = fields.Many2one('time.frame', string='Time frame', required=True)
    delivery_date = fields.Date(related='time_frame_id.delivery_date', store=True)
    lines = fields.One2many('delivery.round.line', 'delivery_round', string='Delivery line')
    deliverer = fields.Many2one('res.users', string="Deliverer")
    responsible = fields.Many2one('res.users', string="Responsible")
    state = fields.Selection([('draft','Draft'),
                              ('ready','Ready'),
                              ('done','Done')], string="State", default="draft")
    
    @api.one
    def action_ready(self):
         self.write({'state':'ready'})
    
    @api.one
    def action_done(self):
        self.write({'state':'done'})
    
class DeliveryRoundLine(models.Model):    
    _name = "delivery.round.line"
    
    sequence = fields.Integer(string="Sequence")
    delivery_round = fields.Many2one('delivery.round', string="Delivery round", required=True)
    raliment_point = fields.Many2one('res.partner', string="R'Aliment point")
    delivery_address = fields.Many2one('res.partner', string="Delivery adress", domain=[('type','=','delivery')])
    picking_wave = fields.Many2one('stock.picking.wave', string="Picking wave")
    stock_pickings = fields.One2many(related='picking_wave.picking_ids', string="Stock pickings")
    