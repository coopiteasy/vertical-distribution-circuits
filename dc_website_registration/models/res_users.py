# Copyright 2017 Coop IT Easy SCRLfs
#     Houssine Bakkali <houssine@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models
from odoo.addons.auth_signup.models.res_partner import SignupError


class ResUsers(models.Model):

    _inherit = "res.users"

    need_validation = fields.Boolean(string="Need validation")
