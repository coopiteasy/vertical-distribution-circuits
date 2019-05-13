# Copyright 2019 Coop IT Easy SCRLfs
#     Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class TimeFrame(models.Model):
    _inherit = 'time.frame'

    preset_cart_id = fields.Many2one(
        comodel_name='preset.cart',
        string='Preset Cart')

    preset_cart_line_ids = fields.One2many(
        comodel_name='preset.cart.line',
        related='preset_cart_id.cart_line_ids',
    )
