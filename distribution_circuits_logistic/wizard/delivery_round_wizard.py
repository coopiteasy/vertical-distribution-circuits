# -*- coding: utf-8 -*-
from odoo import models, fields, api


class DeliveryRoundWizard(models.TransientModel):

    _name = "delivery.round.wizard"

    time_frame_id = fields.Many2one('time.frame',
                                    string="Time Frame",
                                    domain=[('state', '=', 'closed')],
                                    required=True)

    @api.one
    def run_delivery_scheduler(self):
        time_frame = self.time_frame_id

        pickings = self.env['stock.picking'].search([
            ('time_frame_id.id', '=', time_frame.id), ('batch_id', '=', None)])

        if len(pickings) > 0:
            delivery_round = self.env['delivery.round'].search(
                [('time_frame_id.id', '=', time_frame.id)])

            if len(delivery_round) == 0:
                delivery_round = self.env['delivery.round'].create(
                    {'time_frame_id': time_frame.id})

            for picking in pickings:
                wave_found = False
                for line in delivery_round.lines:
                    if picking.delivery_address == line.delivery_address:
                        picking.batch_id = line.picking_batch.id
                        wave_found = True
                        break
                if not wave_found:
                    new_batch = self.env['stock.picking.batch'].create(
                        {'name': 'Lalalalala'})
                    picking.batch_id = new_batch.id
                    self.env['delivery.round.line'].create(
                        {'delivery_round': delivery_round.id,
                         'delivery_address': picking.delivery_address.id,
                         'raliment_point': picking.raliment_point.id,
                         'picking_batch': new_batch.id})

        return True
