# -*- coding: utf-8 -*-
# © 2017 Houssine BAKKALI, Coop IT Easy
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockPicking(models.Model):

    _inherit = "stock.picking"

    time_frame_id = fields.Many2one(
        compute="_compute_time_frame",
        comodel_name="time.frame",
        string="Time Frame",
        store=True)
    raliment_point = fields.Many2one(
        compute="_compute_partners",
        comodel_name="res.partner",
        string="Raliment Point",
        domain=[('is_raliment_point', '=', True)],
        store=True)
    delivery_address = fields.Many2one(
        compute="_compute_partners",
        comodel_name="res.partner",
        string="Delivery address",
        store=True)
    partner_id = fields.Many2one(
        compute="_compute_partners",
        comodel_name="res.partner",
        string='Partner',
        store=True,
        readonly=True)

    @api.multi
    @api.depends('move_lines')
    def _compute_partners(self):
        so_obj = self.env['sale.order']
        for picking in self:
            if picking.sale_id:
                picking.raliment_point = picking.sale_id.raliment_point
                picking.partner_id = picking.sale_id.partner_id
                picking.delivery_address = picking.sale_id.partner_shipping_id
            else:
                so = so_obj.sudo().search([('name', '=', picking.origin)])
                picking.raliment_point = so.raliment_point
                picking.partner_id = so.partner_id
                picking.delivery_address = so.partner_shipping_id

    @api.multi
    @api.depends('move_lines')
    def _compute_time_frame(self):
        so_obj = self.env['sale.order']
        for picking in self:
            if picking.sale_id:
                picking.time_frame_id = picking.sale_id.time_frame_id.id
            else:
                so = so_obj.sudo().search([('name', '=', picking.origin)])
                picking.time_frame_id = so.time_frame_id


class StockPickingBatch(models.Model):

    _inherit = "stock.picking.batch"

    round_line = fields.One2many(
        'delivery.round.line',
        'picking_batch',
        string="Delivery round line")


class StockMoveLine(models.Model):

    _inherit = "stock.move.line"

    raliment_point = fields.Many2one(
        related="picking_id.raliment_point",
        string="Raliment Point",
        store=True)
    delivery_address = fields.Many2one(
        related="picking_id.delivery_address",
        string="Delivery Address",
        store=True)
