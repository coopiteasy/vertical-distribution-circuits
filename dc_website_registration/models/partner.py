# Copyright 2017 Coop IT Easy SCRLfs
#     Houssine Bakkali <houssine@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from ast import literal_eval
from odoo.tools.misc import ustr

from odoo import api, models
from odoo.addons.auth_signup.models.res_partner import SignupError


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def signup_retrieve_info(self, token):
        res = super(ResPartner, self).signup_retrieve_info(token)
        partner = self.sudo().search([('email', '=', res.get('login'))])
        rp = partner.raliment_point_id
        dp = partner.delivery_point_id

        res['lastname'] = partner.lastname
        res['firstname'] = partner.firstname
        res['raliment_point_id'] = rp.id if len(rp) > 0 else 0
        res['delivery_point_id'] = dp.id if len(dp) > 0 else 0
        res['phone'] = partner.phone
        res['zip_code'] = partner.zip
        res['street'] = partner.street
        res['city'] = partner.city
        res['raliment_points'] = self.sudo().get_raliment_points()
        res['delivery_points'] = self.sudo().get_delivery_points()
        res['countries'] = self.env['res.country'].sudo().search([])
        res['country_id'] = '21'

        return res

    @api.model
    def _signup_create_user(self, values):
        """ create a new user from the template user """
        get_param = self.env['ir.config_parameter'].sudo().get_param
        template_user_id = literal_eval(get_param('auth_signup.template_user_id', 'False'))
        template_user = self.browse(template_user_id)
        assert template_user.exists(), 'Signup: invalid template user'

        # check that uninvited users may sign up
        if 'partner_id' not in values:
            if not literal_eval(get_param('auth_signup.allow_uninvited', 'False')):
                raise SignupError(_('Signup is not allowed for uninvited users'))

        assert values.get('login'), "Signup: no login given for new user"
        assert values.get('partner_id') or values.get('lastname') or values.get('firstname'), "Signup: no lastname, firstname or partner given for new user"

        # create a copy of the template user (attached to a specific partner_id if given)
        values['active'] = True
        try:
            with self.env.cr.savepoint():
                return template_user.with_context(no_reset_password=True).copy(values)
        except Exception as e:
            # copy may failed if asked login is not available.
            raise SignupError(ustr(e))
