# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class TimeFrame(models.Model):

    _inherit = "time.frame"

    pickings_consolidation = fields.One2many('picking.consolidation',
                                             'time_frame_id',
                                             string="Picking consolidation")

    @api.one
    def action_consolidate(self):
        pick_consol_line_obj = self.env['picking.consolidation.line']
        time_frame_consol_obj = self.env['time.frame.consolidation']
        consol_obj = self.env['picking.consolidation']
        sup_consol_obj = self.env['picking.supplier.consolidation']
        cust_consol_obj = self.env['picking.customer.consolidation']
        cust_consol_line_obj = self.env['customer.consolidation.line']
        supplier_consol_line_obj = self.env['supplier.consolidation.line']
        delivery_round_obj = self.env['delivery.round']
        delivery_round_line_obj = self.env['delivery.round.line']
        picking_batch_obj = self.env['stock.picking.batch']

        pickings = self.env['stock.picking'].search([
            ('time_frame_id.id', '=', self.id), ('batch_id', '=', None)])

        if self.state == 'closed':
            if len(pickings) > 0:
                delivery_round = delivery_round_obj.search(
                    [('time_frame_id.id', '=', self.id)])

                if len(delivery_round) == 0:
                    delivery_round = delivery_round_obj.create(
                        {'time_frame_id': self.id})

                for picking in pickings:
                    wave_found = False
                    for line in delivery_round.lines:
                        if picking.delivery_address == line.delivery_address:
                            picking.batch_id = line.picking_batch.id
                            wave_found = True
                            break
                    if not wave_found:
                        pick_batch_seq = self.env.ref('distribution_circuits_logistic.sequence_stock_picking_batch', False)
                        name = pick_batch_seq.next_by_id()
                        new_batch = picking_batch_obj.create({'name': name})
                        picking.batch_id = new_batch.id
                        delivery_round_line_obj.create(
                            {'delivery_round': delivery_round.id,
                             'delivery_address': picking.delivery_address.id,
                             'raliment_point': picking.raliment_point.id,
                             'picking_batch': new_batch.id})

                time_frame_consol = time_frame_consol_obj.search(
                    [('time_frame_id', '=', self.id)])

                if len(time_frame_consol) == 0:
                    time_frame_consol = time_frame_consol_obj.create(
                        {'time_frame_id': self.id,
                         'delivery_round': delivery_round.id})
                if len(time_frame_consol.picking_consolidations) > 0:
                    time_frame_consol.picking_consolidations.unlink()
                if len(time_frame_consol.picking_supplier_consolidation) > 0:
                    time_frame_consol.picking_supplier_consolidation.unlink()
                if len(time_frame_consol.picking_customer_consolidation) > 0:
                    time_frame_consol.picking_customer_consolidation.unlink()

                supplier_consols = {}
                customer_consols = {}
                for delivery_line in delivery_round.lines:
                    product_consols = {}
                    for picking in delivery_line.picking_batch.picking_ids:
                        if picking.partner_id.raliment_point_id:
                            raliment_point = picking.partner_id.raliment_point_id
                            customer = picking.partner_id
                            for pack_op in picking.move_lines:
                                # raliment consolidation
                                if product_consols.get(pack_op.product_id):
                                    product_consols[pack_op.product_id][0] += pack_op.product_uom_qty
                                else:
                                    product_consols[pack_op.product_id] = [pack_op.product_uom_qty, pack_op.product_uom, 0]

                                # supplier consolidation
                                supplier = pack_op.product_id.product_tmpl_id.supplier_id
                                if not supplier_consols.get(supplier):
                                    supplier_consols[supplier] = {}
                                if not supplier_consols.get(supplier).get(raliment_point):
                                    supplier_consols[supplier][raliment_point] = {}
                                if (supplier_consols.get(supplier) and 
                                    supplier_consols.get(supplier).get(raliment_point) and
                                    supplier_consols.get(supplier).get(raliment_point).get(pack_op.product_id)):
                                    supplier_consols[supplier][raliment_point][pack_op.product_id][0] += pack_op.product_uom_qty
                                else:
                                    supplier_consols[supplier][raliment_point][pack_op.product_id] = [pack_op.product_uom_qty, pack_op.product_uom,0]

                                # customer consolidation
                                if not customer_consols.get(raliment_point):
                                    customer_consols[raliment_point] = {}
                                if not customer_consols.get(raliment_point).get(customer):
                                    customer_consols[raliment_point][customer] = {}
                                if (customer_consols.get(raliment_point) and
                                    customer_consols.get(raliment_point).get(customer) and
                                    customer_consols.get(raliment_point).get(customer).get(pack_op.product_id)):
                                    customer_consols[raliment_point][customer][pack_op.product_id][0] += pack_op.product_uom_qty
                                else:
                                    customer_consols[raliment_point][customer][pack_op.product_id] = [pack_op.product_uom_qty, pack_op.product_uom, 0]
                    # raliment consolidation
                    if len(product_consols) > 0:
                        picking_consol = consol_obj.create(
                            {'time_frame_consolidation_id': time_frame_consol.id,
                             'delivery_address': delivery_line.picking_batch.round_line.delivery_address.id})
                        for product_id, product_consol in product_consols.items():
                            pick_consol_line_obj.create(
                                {'picking_consolidation_id': picking_consol.id,
                                 'product_id': product_id.id,
                                 'product_uom_qty': product_consol[0],
                                 'product_uom': product_consol[1].id,
                                 'qty_delivered': product_consol[2]})
                # supplier consolidation
                for supplier, raliment_point_consols in supplier_consols.items():
                        supplier_consol = sup_consol_obj.create({
                            'time_frame_consolidation_id': time_frame_consol.id,
                            'supplier': supplier.id
                            })
                        for rali_point, prod_consols in raliment_point_consols.items():
                            for product, prod_quant in prod_consols.items():
                                supplier_consol_line_obj.create({
                                    'supplier_consolidation_id': supplier_consol.id,
                                    'raliment_point_id': rali_point.id,
                                    'product_id': product.id,
                                    'product_uom_qty': prod_quant[0],
                                    'product_uom': prod_quant[1].id,
                                    'qty_delivered': prod_quant[2]
                                    })
                # customer consolidation
                for raliment_point, cust_consols in customer_consols.items():
                        cust_consol = cust_consol_obj.create(
                            {'time_frame_consolidation_id': time_frame_consol.id,
                             'delivery_address': raliment_point.id})
                        for customer, prod_consols in cust_consols.items():
                            for product, prod_quant in prod_consols.items():
                                cust_consol_line_obj.create({
                                    'customer_consolidation_id': cust_consol.id,
                                    'customer_id': customer.id,
                                    'supplier_id': product.product_tmpl_id.supplier_id.id,
                                    'product_id': product.id,
                                    'product_uom_qty': prod_quant[0],
                                    'product_uom': prod_quant[1].id,
                                    'qty_delivered': prod_quant[2]
                                    })
        else:
            raise UserError(_('You can only run a consolidation on a '
                              'closed time frame.'))
