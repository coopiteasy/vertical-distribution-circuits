# Copyright 2019 Coop IT Easy SCRLfs
#     Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _
from odoo.exceptions import UserError


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
    suspend_cart = fields.Boolean(
        string='Suspend cart')
    cart_suspended_from = fields.Date(
        string='Cart Suspended from')
    cart_suspended_date = fields.Date(
        string='Cart Suspended Until',
    )

    @api.model
    def is_subscribed(self, date=None):
        self.ensure_one()

        date = date if date else fields.Date.today()
        suspended = bool(
            self.suspend_cart 
            and date <= self.cart_suspended_date
            and date >= self.cart_suspended_from)

        return self.subscription_id and not suspended

    @api.model  # todo necessary ?
    def get_subscriptions(self):
        return self.env['subscription'].search([('active', '=', True)])

    @api.model
    def signup_retrieve_info(self, token):
        res = super(ResPartner, self).signup_retrieve_info(token)

        partner = self.sudo().search([('email', '=', res.get('login'))])

        res['subscription_id'] = partner.subscription_id.id if len(partner.subscription_id) > 0 else 0
        res['nb_household'] = partner.nb_household
        res['subscriptions'] = self.sudo().get_subscriptions()
        return res

    @api.multi
    def write(self, vals):
        for partner in self:
            if 'cart_suspended_from' in vals and 'cart_suspended_date' in vals:
                suspended_from = vals['cart_suspended_from']
                suspended_to = vals['cart_suspended_date']
            elif 'cart_suspended_from' in vals:
                suspended_from = vals['cart_suspended_from']
                suspended_to = partner.cart_suspended_date
            elif 'cart_suspended_date' in vals:
                suspended_from = partner.cart_suspended_from
                suspended_to = vals['cart_suspended_date']
            else:
                return super(ResPartner, partner).write(vals)
            if suspended_from > suspended_to:
                raise UserError(_("Cart Suspended from date can't be after Cart Suspended Until date."))
            return super(ResPartner, partner).write(vals)
