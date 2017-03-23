# -*- coding: utf-8 -*-

from openerp import api, fields, models, _

class SaleOrder(models.Model):
    
    _inherit = "sale.order"
    
    raliment_point = fields.Many2one(compute="_compute_raliment", comodel_name="res.partner", string="Raliment Point", domain=[('is_raliment_point','=',True)],store=True)
    time_frame_id = fields.Many2one('time.frame', string="Time Frame")
    
    @api.multi
    @api.depends('partner_id')
    def _compute_raliment(self):
        for order in self:
            if order.partner_id.parent_id and order.partner_id.parent_id.raliment_point:
                order.raliment_point = order.partner_id.parent_id
