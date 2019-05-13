# Copyright 2019 Coop IT Easy SCRLfs
#     Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
import datetime as dt


class PresetCart(models.Model):
    _name = 'preset.cart'

    time_frame_ids = fields.One2many(
        comodel_name='time.frame',
        inverse_name='preset_cart_id',
        string='Time Frames',
        required=True)
    name = fields.Char(
        string='Name',
        default=lambda x: dt.datetime.now().strftime('%Y-W%W'))
    cart_line_ids = fields.One2many(
        comodel_name='preset.cart.line',
        string='Cart Lines',
        inverse_name='cart_id',
        required=False,
        delete='cascade')


class PresetCartLine(models.Model):
    _name = 'preset.cart.line'
    
    cart_id = fields.Many2one(
        comodel_name='preset.cart',
        string='Preset Cart',
        required=True)
    product_id = fields.Many2one(
        comodel_name='product.template',
        string='Product',
        required=True)
    quantity = fields.Float(
        string='Quantity')
    uom_id = fields.Many2one(
        comodel_name='product.uom',
        related='product_id.uom_id',
        string='Unit of Measure',
        readonly=True)
