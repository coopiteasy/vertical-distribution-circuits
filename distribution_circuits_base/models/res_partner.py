# -*- coding: utf-8 -*-
from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    is_gac = fields.Boolean(string="Est un GAC")
    is_raliment_point = fields.Boolean(string="Is a gathering point")
    is_delivery_point = fields.Boolean(string="Is a delivery point")
    raliment_point_id = fields.Many2one(
        'res.partner',
        string="Point de Raliment",
        domain=[('is_raliment_point', '=', True)])
    raliment_point_manager = fields.Many2one(
        'res.users',
        string="Raliment point responsible",
        domain=[('share', '=', False)])
    delivery_point_id = fields.Many2one(
        'res.partner',
        string="Delivery Point",
        domain=[('is_delivery_point', '=', True)])

    @api.multi
    def address_get(self, adr_pref=None):
        result = super(ResPartner, self).address_get(adr_pref)
        if self.delivery_point_id:
            result['delivery'] = self.delivery_point_id.id
        return result

    def get_delivery_address(self):
        if len(self.child_ids) > 0:
            return self.env['res.partner'].search(
                [('id', 'in', self.child_ids.ids), ('type', '=', "delivery")],
                limit=1)

    def get_delivery_points(self):
        return self.env['res.partner'].search(
            [('is_delivery_point', '=', True)])

    def get_raliment_points(self):
        return self.env['res.partner'].search(
            [('is_raliment_point', '=', True)])
