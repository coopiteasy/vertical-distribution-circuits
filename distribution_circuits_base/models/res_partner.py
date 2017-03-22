# -*- coding: utf-8 -*-

from openerp import api, fields, models, _


class ResPartner(models.Model):
    _inherit = "res.partner"
    
    gac = fields.Boolean(string="GAC")
    raliment_point = fields.Boolean(string="Point de Raliment") 
    
    def get_delivery_address(self):
        if len(self.child_ids) > 0:
            return self.env['res.partner'].search([('id','in',self.child_ids.ids),('type','=',"delivery")], limit=1)
            