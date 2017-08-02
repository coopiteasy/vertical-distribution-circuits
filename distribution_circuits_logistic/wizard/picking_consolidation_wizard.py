# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.exceptions import UserError

class DeliveryRoundWizard(models.TransientModel):
    
    _name="picking.consolidation.wizard"
    
    time_frame_id = fields.Many2one('time.frame', string="Time Frame", domain=[('state','=', 'closed')], required=True)
    
    @api.one
    def compute_consolidation(self):
        if self.time_frame_id.state == 'closed':
            delivery_round = self.env['delivery.round'].search([('time_frame_id.id','=',self.time_frame_id.id)])
            time_frame_consol_obj = self.env['time.frame.consolidation']
            consol_obj = self.env['picking.consolidation']
            pick_consol_line_obj = self.env['picking.consolidation.line']
            sup_consol_obj = self.env['picking.supplier.consolidation']
            supplier_consol_line_obj = self.env['supplier.consolidation.line']
            cust_consol_obj = self.env['picking.customer.consolidation']
            cust_consol_line_obj = self.env['customer.consolidation.line']
            time_frame_consol = time_frame_consol_obj.search([('time_frame_id','=',self.time_frame_id.id)])
            
            if len(time_frame_consol) == 0:
                time_frame_consol = time_frame_consol_obj.create({'time_frame_id':self.time_frame_id.id,
                                                                  'delivery_round':delivery_round.id})
            if len(time_frame_consol.picking_consolidations) > 0:
                time_frame_consol.picking_consolidations.unlink()
            if len(time_frame_consol.picking_supplier_consolidation) > 0:
                time_frame_consol.picking_supplier_consolidation.unlink()
            if len(time_frame_consol.picking_customer_consolidation) > 0:
                time_frame_consol.picking_customer_consolidation.unlink()
            if len(delivery_round) > 0:
                supplier_consols = {}
                customer_consols = {}
                for delivery_line in delivery_round.lines:
                    product_consols = {}
                    for picking in delivery_line.picking_wave.picking_ids:
                        if picking.partner_id.raliment_point_id:
                            raliment_point = picking.partner_id.raliment_point_id
                            customer = picking.partner_id
                            for pack_operation in picking.move_lines:
                                # raliment consolidaiton
                                if product_consols.get(pack_operation.product_id):
                                    product_consols[pack_operation.product_id][0] += pack_operation.product_uom_qty
                                    #product_consols[pack_operation.product_id][2] += pack_operation.qty_done
                                else:
                                    #product_consols[pack_operation.product_id] = [pack_operation.product_qty, pack_operation.product_uom_id, pack_operation.qty_done]
                                    product_consols[pack_operation.product_id] = [pack_operation.product_uom_qty, pack_operation.product_uom, 0]
                                
                                # supplier consolidation
                                supplier = pack_operation.product_id.product_tmpl_id.supplier_id
                                if not supplier_consols.get(supplier):
                                    supplier_consols[supplier] = {}
                                if not supplier_consols.get(supplier).get(raliment_point):
                                    supplier_consols[supplier][raliment_point] = {}
                                if (supplier_consols.get(supplier) and 
                                    supplier_consols.get(supplier).get(raliment_point) and
                                    supplier_consols.get(supplier).get(raliment_point).get(pack_operation.product_id)):
                                    supplier_consols[supplier][raliment_point][pack_operation.product_id][0] += pack_operation.product_uom_qty
                                    #supplier_consols[supplier][raliment_point][pack_operation.product_id][2] += pack_operation.qty_done
                                else:
                                    #supplier_consols[supplier][raliment_point][pack_operation.product_id] = [pack_operation.product_qty, pack_operation.product_uom_id,pack_operation.qty_done]
                                    supplier_consols[supplier][raliment_point][pack_operation.product_id] = [pack_operation.product_uom_qty, pack_operation.product_uom,0]
                                
                                # customer consolidation
                                if not customer_consols.get(raliment_point):
                                    customer_consols[raliment_point] = {}
                                if not customer_consols.get(raliment_point).get(customer):
                                    customer_consols[raliment_point][customer] = {}
                                if (customer_consols.get(raliment_point) and 
                                    customer_consols.get(raliment_point).get(customer) and
                                    customer_consols.get(raliment_point).get(customer).get(pack_operation.product_id)):
                                    customer_consols[raliment_point][customer][pack_operation.product_id][0] += pack_operation.product_uom_qty
                                    #customer_consols[raliment_point][customer][pack_operation.product_id][2] += pack_operation.qty_done
                                else:
                                    #customer_consols[raliment_point][customer][pack_operation.product_id] = [pack_operation.product_qty, pack_operation.product_uom_id,pack_operation.qty_done]
                                    customer_consols[raliment_point][customer][pack_operation.product_id] = [pack_operation.product_uom_qty, pack_operation.product_uom,0]
                    # raliment consolidation
                    if len(product_consols) > 0:
                        picking_consol = consol_obj.create({'time_frame_consolidation_id':time_frame_consol.id,
                                                            'delivery_address':delivery_line.picking_wave.round_line.delivery_address.id})
                        for product_id, product_consol in product_consols.items():
                            pick_consol_line_obj.create({'picking_consolidation_id':picking_consol.id,
                                                     'product_id':product_id.id,
                                                     'product_uom_qty':product_consol[0],
                                                     'product_uom':product_consol[1].id,
                                                     'qty_delivered':product_consol[2]})
                # supplier consolidation
                for supplier, raliment_point_consols in supplier_consols.items():
                        supplier_consol = sup_consol_obj.create({'time_frame_consolidation_id':time_frame_consol.id,
                                                            'supplier':supplier.id})
                        for rali_point, prod_consols in raliment_point_consols.items():
                            for product, prod_quant in prod_consols.items():
                                supplier_consol_line_obj.create({'supplier_consolidation_id':supplier_consol.id,
                                                     'raliment_point_id':rali_point.id,
                                                     'product_id':product.id,
                                                     'product_uom_qty':prod_quant[0],
                                                     'product_uom':prod_quant[1].id,
                                                     'qty_delivered':prod_quant[2]})
                # customer consolidation
                for raliment_point, cust_consols in customer_consols.items():
                        cust_consol = cust_consol_obj.create({'time_frame_consolidation_id':time_frame_consol.id,
                                                            'delivery_address':raliment_point.id})
                        for customer, prod_consols in cust_consols.items():
                            for product, prod_quant in prod_consols.items():
                                cust_consol_line_obj.create({'customer_consolidation_id':cust_consol.id,
                                                     'customer_id':customer.id,
                                                     'supplier_id':product.product_tmpl_id.supplier_id.id,
                                                     'product_id':product.id,
                                                     'product_uom_qty':prod_quant[0],
                                                     'product_uom':prod_quant[1].id,
                                                     'qty_delivered':prod_quant[2]})
            else:
                raise UserError(_('You have to generate the delivery round wizard before to run this process.'))
        else:
            raise UserError(_('You can only run a consolidation on a closed time frame.'))

