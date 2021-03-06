# -*- coding: utf-8 -*-

from odoo import api, fields, models


class DeliveryRound(models.Model):

    _name = "delivery.round"

    name = fields.Char(string="Name", required=True, default="/")
    deliverer = fields.Many2one('res.users', string="Deliverer")
    responsible = fields.Many2one('res.users', string="Responsible")
    time_frame_id = fields.Many2one(
        'time.frame',
        string='Time frame',
        required=True)
    delivery_date = fields.Date(related='time_frame_id.delivery_date',
                                store=True)
    lines = fields.One2many('delivery.round.line', 'delivery_round',
                            string='Delivery line')
    state = fields.Selection([('draft', 'Draft'),
                              ('ready', 'Ready'),
                              ('done', 'Done')],
                             string="State", default="draft")

    @api.one
    def action_ready(self):
        self.write({'state': 'ready'})

    @api.one
    def action_done(self):
        self.write({'state': 'done'})


class DeliveryRoundLine(models.Model):

    _name = "delivery.round.line"

    sequence = fields.Integer(string="Sequence")
    delivered = fields.Boolean(string="Delivered")
    picking_batch = fields.Many2one('stock.picking.batch',
                                    string="Picking batch")
    delivery_round = fields.Many2one('delivery.round', string="Delivery round",
                                     required=True)
    raliment_point = fields.Many2one('res.partner',
                                     string="R'Aliment point")
    delivery_address = fields.Many2one(
        'res.partner',
        string="Delivery address",
        domain=[('is_delivery_point', '=', True)])
    stock_pickings = fields.One2many(related='picking_batch.picking_ids',
                                     string="Stock pickings")
    order_quantity = fields.Integer(string="Order quantity",
                                    compute="_compute_order_quantity",
                                    store=True)

    @api.depends('stock_pickings')
    @api.multi
    def _compute_order_quantity(self):
        for line in self:
            line.order_quantity = len(line.stock_pickings)
