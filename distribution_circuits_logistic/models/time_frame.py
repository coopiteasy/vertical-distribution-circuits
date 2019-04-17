# -*- coding: utf-8 -*-
from odoo import api, fields, models


class TimeFrame(models.Model):

    _inherit = "time.frame"

    pickings_consolidation = fields.One2many('picking.consolidation',
                                             'time_frame_id',
                                             string="Picking consolidation")
