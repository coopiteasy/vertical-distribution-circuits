# -*- coding: utf-8 -*-

from openerp import api, fields, models, _

class ResUsers(models.Model):
    _inherit = "res.users"
    
    need_validation = fields.Boolean(string="Need validation")