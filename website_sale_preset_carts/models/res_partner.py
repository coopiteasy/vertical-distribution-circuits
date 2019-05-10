# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRLfs
#     Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    nb_household = fields.Integer(
        string='Number of People in Household',
    )
    cart_subscription = fields.Boolean(
        string='Is Subscribed to Cart',
    )
    cart_suspended_date = fields.Date(
        string='Cart Suspended Until',
    )

