# -*- coding: utf-8 -*-
# © 2016 Coop IT Easy (http://www.coopiteasy.be)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api
from openerp.addons.web.http import request

class WebSite(models.Model):
    _inherit = 'website'
    
    current_time_frame = fields.Many2one('time.frame', string='Selected time frame')
    
    def get_current_time_frame(self):
        #current_time_frame = request.session.get('selected_time_frame')
        #return self.env['time.frame'].browse(int(current_time_frame)).id
        return request.session.get('selected_time_frame')
    
    @api.multi 
    def get_open_time_frames(self):
        res = []
        for time_frame in self.env['time.frame'].sudo().search([('state','=','open')]): 
            res.append((time_frame.id,time_frame.name))
        return res
    
    @api.multi
    def sale_get_order(self, force_create=False, code=None, update_pricelist=False, force_pricelist=False, context=None):
        sale_order = super(WebSite, self).sale_get_order(force_create=False, code=None, update_pricelist=False, force_pricelist=False, context=None) 
        if sale_order and not sale_order.time_frame_id and request.session.get('selected_time_frame'):
            sale_order.time_frame_id = int(request.session.get('selected_time_frame'))
        return sale_order
    
    @api.multi
    def sale_product_domain(self):
        domain = super(WebSite, self).sale_product_domain()
        #won't work
#         if 'time_frame_id' in self.env.context:
#             domain.append(
#                 ('time_frame_id', '=', self.env.context['time_frame_id']))
        return domain
