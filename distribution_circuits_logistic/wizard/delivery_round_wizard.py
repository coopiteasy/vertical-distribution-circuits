from openerp import models, fields, api

class DeliveryRoundWizard(models.TransientModel):
    
    _name="delivery.round.wizard"
    
    time_frame_id = fields.Many2one('time.frame', string="Time Frame", domaine=[('state','=', 'open')], required=True)
    
    @api.one
    def run_delivery_scheduler(self):
        time_frame = self.time_frame_id
        pickings = self.env['stock.picking'].search([('time_frame_id.id','=',time_frame.id),('wave_id','=',None)])
        if len(pickings) > 0:
            delivery_round = self.env['delivery.round'].search([('time_frame_id.id','=',time_frame.id)])
            if len(delivery_round) == 0:
                delivery_round = self.env['delivery.round'].create({'time_frame_id':time_frame.id})
            for picking in pickings:
                wave_found = False
                for line in delivery_round.lines:
                    if picking.delivery_address == line.delivery_address:
                        picking.wave_id = line.picking_wave.id
                        wave_found = True
                        break
                if not wave_found:
                    new_wave = self.env['stock.picking.wave'].create()
                    picking.wave_id = new_wave.id
                    new_line = line.create({'round_id':line.round_id,
                                            'delivery_address':picking.delivery_address,
                                            'raliment_point_id':picking.raliment_point,
                                            'picking_wave':new_wave})
            
        return True