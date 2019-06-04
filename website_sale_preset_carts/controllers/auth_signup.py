# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.http import request


class AuthSignupHome(AuthSignupHome):

    def do_signup(self, qcontext):
        uid = super(AuthSignupHome, self).do_signup(qcontext)
        user = request.env['res.users'].sudo().search([('id', '=', uid)])
        user.partner_id.write({
            'nb_household': qcontext.get('nb_household', False),
            'cart_subscription': qcontext.get('cart_subscription', False),
        })


