# -*- coding: utf-8 -*-

from openerp import api, fields, models, _

class SaleOrder(models.Model):
    
    _inherit = "sale.order"
    
    time_frame_id = fields.Many2one('time.frame', string="Time Frame", required=True)