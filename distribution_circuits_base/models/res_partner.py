# -*- coding: utf-8 -*-

from openerp import api, fields, models, _


class ResPartner(models.Model):
    _inherit = "res.partner"
    
    is_gac = fields.Boolean(string="est un GAC")
    is_raliment_point = fields.Boolean(string="Est un Point de Raliment") 
    raliment_point_id = fields.Many2one('res.partner', string="Point de Raliment")
    
    def get_delivery_address(self):
        if len(self.child_ids) > 0:
            return self.env['res.partner'].search([('id','in',self.child_ids.ids),('type','=',"delivery")], limit=1)
            