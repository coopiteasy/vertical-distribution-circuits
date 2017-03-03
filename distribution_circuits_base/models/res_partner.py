# -*- coding: utf-8 -*-

from openerp import api, fields, models, _


class ResPartner(models.Model):
    _inherit = "res.partner"
    
    gac = fields.Boolean(string="GAC")
    raliment_point = fields.Boolean(string="Point de Raliment") 