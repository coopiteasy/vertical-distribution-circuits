import logging
import werkzeug

from odoo import http
from odoo.http import request
from odoo.tools.translate import _
from odoo import tools

from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.addons.base_iban.models import res_partner_bank

from odoo.addons.auth_signup.models.res_partner import SignupError
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class AuthSignupHome(AuthSignupHome):
    def _signup_with_values(self, token, values):
        db, login, password = request.env['res.users'].sudo().signup(values,
                                                                     token)
        # as authenticate will use its own cursor we need to commit
        # the current transaction
        request.cr.commit()
        uid = request.session.authenticate(db, login, password)
        if not uid:
            raise SignupError(_('Authentication Failed.'))
        return uid

    def do_signup(self, qcontext):
        """ Shared helper that creates a res.partner out of a token """
        values = dict((key, qcontext.get(key)) for key in ('login',
                                                           'name',
                                                           'lastname',
                                                           'firstname',
                                                           'password', 'phone',
                                                           'street', 'city',
                                                           'zip_code',
                                                           'country_id',
                                                           'raliment_point_id',
                                                           'delivery_point_id'
                                                           ))
        assert any([k for k in values.values()]), "The form was not properly filled in."
        assert values.get('password') == qcontext.get('confirm_password'), "Passwords do not match; please retype them."
        supported_langs = [lang['code'] for lang in request.env['res.lang'].sudo().search_read([], ['code'])]
        if request.lang in supported_langs:
            values['lang'] = request.lang
        values['zip'] = values['zip_code']
        qcontext['customer'] = True
        qcontext['need_validation'] = True
        uid = self._signup_with_values(qcontext.get('token'), values)
        iban = qcontext.get('iban')
        user = request.env['res.users'].sudo().search([('id', '=', uid)])
        user.partner_id.write({'firstname': values['firstname'],
                               'lastname': values['lastname']})
        request.env['res.partner.bank'].sudo().create(
            {'partner_id': user.partner_id.id, 'acc_number': iban})
        request.cr.commit()

    @http.route('/web/signup', type='http', auth='public', website=True)
    def web_auth_signup(self, *args, **kw):
        qcontext = self.get_auth_signup_qcontext()
        qcontext['name'] = qcontext.get('firstname','') + ' ' + qcontext.get('lastname','')

        if not qcontext.get('raliment_point_id', False) and \
                not qcontext.get('delivery_point_id', False):
            qcontext['error'] = _("You must at least choose a Raliment or a "
                                  "Delivery point")
        if qcontext.get('raliment_point_id', False) and \
                qcontext.get('delivery_point_id', False):
            qcontext['error'] = _("You can not choose a Raliment and a "
                                  "Delivery point")
        if qcontext.get("login", False) and \
                not tools.single_email_re.match(qcontext.get("login", "")):
            qcontext["error"] = _("That does not seem to be an email address.")
        if qcontext.get("iban", False):
            try:
                res_partner_bank.validate_iban(qcontext.get("iban"))
            except ValidationError:
                qcontext["error"] = _("Please give a correct IBAN number.")
        if not qcontext.get('token') and not qcontext.get('signup_enabled'):
            raise werkzeug.exceptions.NotFound()

        if 'error' not in qcontext and request.httprequest.method == 'POST':
            try:
                self.do_signup(qcontext)
                # Send an account creation confirmation email
                if qcontext.get('token'):
                    user_sudo = request.env['res.users'].sudo().search([('login', '=', qcontext.get('login'))])
                    template = request.env.ref('auth_signup.mail_template_user_signup_account_created', raise_if_not_found=False)
                    if user_sudo and template:
                        template.sudo().with_context(
                            lang=user_sudo.lang,
                            auth_login=werkzeug.url_encode({'auth_login': user_sudo.email}),
                        ).send_mail(user_sudo.id)
                return super(AuthSignupHome, self).web_login(*args, **kw)
            except UserError as e:
                qcontext['error'] = e.name or e.value
            except (SignupError, AssertionError) as e:
                if request.env["res.users"].sudo().search([
                        ("login", "=", qcontext.get("login"))]):
                    qcontext["error"] = _("Another user is already registered "
                                          "using this email address.")
                else:
                    _logger.error("%s", e)
                    qcontext['error'] = _("Could not create a new account.")
        if not qcontext.get('raliment_point_id', False):
            qcontext['raliment_point_id'] = 0
        if not qcontext.get('delivery_point_id', False):
            qcontext['delivery_point_id'] = 0
        qcontext['raliment_points'] = request.env['res.partner'].sudo().get_raliment_points()
        qcontext['delivery_points'] = request.env['res.partner'].sudo().get_delivery_points()
        qcontext['countries'] = request.env['res.country'].sudo().search([])
        qcontext['country_id'] = request.env['res.country'].sudo().search([('code','=','BE')]).id

        return request.render('auth_signup.signup', qcontext)
