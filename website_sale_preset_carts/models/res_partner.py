# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRLfs
#     Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
import datetime as dt


class ResPartner(models.Model):
    _inherit = 'res.partner'

    nb_household = fields.Integer(
        string='Number of People in Household',
        default=1,
    )
    subscription_id = fields.Many2one(
        comodel_name='subscription',
        string='Subscription',
        required=False)
    cart_suspended_date = fields.Date(
        string='Cart Suspended Until',
    )

    @api.model
    def is_subscribed(self, date=None):
        date = date if date else dt.date.today()

        self.ensure_one()
        if self.cart_suspended_date:
            suspended = date.today() <= self.cart_suspended_date
        else:
            suspended = False

        return self.subscription_id and not suspended

    @api.model  # todo necessary ?
    def get_subscriptions(self):
        return self.env['subscription'].search([('active', '=', True)])

    @api.model
    def signup_retrieve_info(self, token):
        res = super(ResPartner, self).signup_retrieve_info(token)

        partner = self.sudo().search([('email', '=', res.get('login'))])

        res['subscription_id'] = partner.subscription_id.id if len(partner.subscription_id) > 0 else 0
        res['subscriptions'] = self.sudo().get_subscriptions()
        return res
