# Copyright 2019 Coop IT Easy SCRLfs
#     Robin Keunen <robin@coopiteasy.be>
#     Houssine Bakkali <houssine@coopiteasy.be>
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

    ongoing_subscription = fields.Boolean(
        compute="_compute_ongoing_subscription",
        string="Ongoing subscription ?",
        help="The subscription state for today"
    )

    @api.multi
    def _compute_ongoing_subscription(self):
        for partner in self:
            partner.ongoing_subscription = partner.is_subscribed()

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
    @api.constrains('cart_suspended_from', 'cart_suspended_date')
    def _check_suspended_dates(self):
        for partner in self:
            if partner.cart_suspended_from > partner.cart_suspended_date:
                raise UserError(
                    _("Cart Suspended from date can't be after Cart "
                      "Suspended Until date."))
