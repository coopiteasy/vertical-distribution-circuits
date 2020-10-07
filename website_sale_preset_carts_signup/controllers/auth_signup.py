# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
#   Houssine Bakkali <houssine@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.addons.dc_website_registration.controllers.authsignup import AuthSignupHome
from odoo import http
from odoo.http import request


class AuthSignupHome(AuthSignupHome):

    def do_signup(self, qcontext):
        uid = super(AuthSignupHome, self).do_signup(qcontext)
        user = request.env['res.users'].sudo().search([('id', '=', uid)])
        user.partner_id.write({
            'nb_household': qcontext.get('nb_household', False),
            'subscription_id': qcontext.get('subscription_id', False),
        })
        return uid

    @http.route('/web/signup', type='http', auth='public', website=True)
    def web_auth_signup(self, *args, **kw):
        res = super(AuthSignupHome, self).web_auth_signup(*args, **kw)
        qcontext = res.qcontext
        if not qcontext.get('subscription_id', False):
            qcontext['subscription_id'] = 0
        qcontext['subscriptions'] = (
            request.env['res.partner']
                   .sudo()
                   .get_subscriptions()
        )
        return res
