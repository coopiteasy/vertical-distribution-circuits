# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.exceptions import UserError

class DeliveryRoundWizard(models.TransientModel):
    
    _name="picking.consolidation.wizard"
    
    time_frame_id = fields.Many2one('time.frame', string="Time Frame", domaine=[('state','=', 'open')], required=True)
    
    @api.one
    def compute_consolidation(self):
        if self.time_frame_id.state == 'closed':
            delivery_round = self.env['stock.picking'].search([('time_frame_id.id','=',self.time_frame_id.id)])
            time_frame_consol_obj = self.env['time.frame.consolidation']
            consol_obj = self.env['picking.consolidation']
            pick_consol_line_obj = self.env['picking.consolidation.line']
            time_frame_consol = time_frame_consol_obj.search([('time_frame_id','=',self.time_frame_id.id)])
            if len(time_frame_consol) == 0:
                time_frame_consol = time_frame_consol_obj.create({'time_frame_id':self.time_frame_id.id})
            if len(time_frame_consol.picking_consolidations) > 0:
                time_frame_consol.picking_consolidations.unlink()
            
            delivery_round = self.env['delivery.round'].search([('time_frame_id.id','=',self.time_frame_id.id)])
            if len(delivery_round) > 0:
                for delivery_line in delivery_round.lines:
                    product_consols = {}
                    picking_consol = consol_obj.create({'time_frame_consolidation_id':time_frame_consol.id,
                                                        'delivery_address':delivery_line.picking_wave.round_line.delivery_address.id})
                    for picking in delivery_line.picking_wave.picking_ids:
                        for pack_op in picking.pack_operation_product_ids:
                            if product_consols.get(pack_op.product_id):
                                product_consols[pack_op.product_id][0] += pack_op.product_qty
                            else:
                                product_consols[pack_op.product_id] = (pack_op.product_qty, pack_op.product_uom_id)
                    for product_id, product_consol in product_consols.items():
                        pick_consol_line_obj.create({'picking_consolidation_id':picking_consol.id,
                                                 'product_id':product_id.id,
                                                 'product_uom_qty':product_consol[0],
                                                 'product_uom':product_consol[1].id})
                    
            else:
                raise UserError(_('You have to generate the delivery round wizard before to run this process.'))
        else:
            raise UserError(_('You can only run a consolidation on a closed time frame.'))
#         for picking in wave_id.picking_ids:            
#             delivery_address
#             for pack_op in picking.pack_operation_product_ids:
#                 
#                 vals = {
#                     'product_id':pack_op.product_id.id,
#                     'product_uom':pack_op.product_uom_id.id,
#                     #'product_uom_qty':pack_op.product_qty,
#                     #'qty_delivered':pack_op.product_qty,
#                 }
