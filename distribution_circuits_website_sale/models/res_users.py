# -*- coding: utf-8 -*-

from openerp import api, fields, models, _

class ResUsers(models.Model):
    _inherit = "res.users"
    
    need_validation = fields.Boolean(string="Need validation")

class ResPartner(models.Model):
    _inherit = "res.partner"
    
    @api.model    
    def signup_retrieve_info(self, token):
        res = super(ResPartner, self).signup_retrieve_info(token)
        partner = self.sudo().search([('email','=',res.get('login'))])
        
        res['raliment_point_id'] = partner.raliment_point_id.id if len(partner.raliment_point_id) > 0 else 0
        res['delivery_point_id'] = partner.delivery_point_id.id if len(partner.delivery_point_id) > 0 else 0
        res['phone'] = partner.phone
        res['zip_code'] = partner.zip
        res['street'] = partner.street
        res['city'] = partner.city
        res['raliment_points'] = self.sudo().get_raliment_points()
        res['delivery_points'] = self.sudo().get_delivery_points()
        res['countries'] = self.env['res.country'].sudo().search([])
        res['country_id'] = '21'
        
        return res