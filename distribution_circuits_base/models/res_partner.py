# -*- coding: utf-8 -*-

from openerp import api, fields, models, _


class ResPartner(models.Model):
    _inherit = "res.partner"
    
    is_gac = fields.Boolean(string="Est un GAC")
    is_raliment_point = fields.Boolean(string="Est un Point de Raliment")
    is_delivery_point = fields.Boolean(string="Est un Point de livraison")
    raliment_point_id = fields.Many2one('res.partner', string="Point de Raliment", domain=[('is_raliment_point','=',True)])
    raliment_point_manager = fields.Many2one('res.users', string="Raliment point responsible", domain=[('share','=',False)])
    delivery_point_id = fields.Many2one('res.partner', string="Delivery Point", domain=[('is_delivery_point','=',True)])
    
    def get_delivery_address(self):
        if len(self.child_ids) > 0:
            return self.env['res.partner'].search([('id','in',self.child_ids.ids),('type','=',"delivery")], limit=1)
        
    def get_delivery_points(self):
        return self.env['res.partner'].search([('is_delivery_point','=',True)])   