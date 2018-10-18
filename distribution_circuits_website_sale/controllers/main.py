import logging

from odoo import http
from odoo.http import request
from odoo.tools.translate import _
from odoo import tools
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.portal.controllers.portal import CustomerPortal

from odoo.addons.auth_signup.models.res_partner import SignupError
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.addons.base_iban.models import res_partner_bank

from odoo.exceptions import ValidationError
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class WebsiteSale(WebsiteSale):

    @http.route([
        '/shop',
        '/shop/page/<int:page>',
        '/shop/category/<model("product.public.category"):category>',
        '/shop/category/<model("product.public.category"):category>/page/<int:page>',
        '/shop/time_frame'
    ], type='http', auth='user', website=True)
    def shop(self, page=0, category=None, time_frame=None, search='', **post):
        time_frames = request.env['time.frame'].sudo().search([
            ('state', '=', 'open')])
        if len(time_frames) == 0:
            return request.render(
                "distribution_circuits_website_sale.shop_closed", post)
        else:
            return super(WebsiteSale, self).shop(page=page, category=category,
                                                 time_frame=time_frame,
                                                 search=search,
                                                 **post)

    @http.route(['/shop/set_current_time_frame'],
                type='json',
                auth="public",
                methods=['POST'],
                website=True)
    def set_current_time_frame(self, time_frame_id=None, **kw):
        env = request.env
        if time_frame_id:
            time_frame = env['time.frame'].sudo().browse(int(time_frame_id))
            if request.website.sale_get_order():
                order = request.website.sale_get_order()
                request.session['selected_time_frame'] = time_frame.id

                # don't update the time frame on the sale order and invalidate the
                # cart(sale order) if it's not in draft state 
                # then return to the shop
                if order.state != 'draft':
                    request.session.update({
                        'sale_order_id': False,
                        'sale_transaction_id': False,
                        'website_sale_current_pl': False,
                    })
                    request.redirect('/shop')
                else:
                    order.sudo().write({'time_frame_id': time_frame.id})
                    return {time_frame.id: time_frame.name}
        else:
            request.session['selected_time_frame'] = None
        return {0: ""}

    @http.route('/shop/payment/validate',
                type='http',
                auth="public",
                website=True)
    def payment_validate(self, transaction_id=None, sale_order_id=None,
                         **post):
        if transaction_id is None:
            tx = request.website.sale_get_transaction()
        else:
            tx = request.env['payment.transaction'].sudo().browse(
                transaction_id)

        if sale_order_id is None:
            order = request.website.sale_get_order()
        else:
            order = request.env['sale.order'].sudo().browse(sale_order_id)
            assert order.id == request.session.get('sale_last_order_id')

        # sometime without knowing yet why we loose the order so we add this
        # last attempt to get the current sale order
        if not order:
            order = request.website.sale_get_order()
            # if it still not defined we redirect to the shop
            if not order:
                _logger.error('The order is not defined')
                if tx:
                    _logger.error('The transaction was reference %s' %
                                  (tx.reference))
                return request.redirect('/shop')

        if order.check_customer_credit():
            if tx:
                tx.write({'state': 'done'})
            return super(WebsiteSale, self).payment_validate(transaction_id,
                                                             sale_order_id,
                                                             **post)
        else:
            _logger.error('The customer credit is not sufficient to cover the payment %s set as error' % (tx.reference))
            return request.redirect('/shop')

    def get_delivery_points(self):
        return request.env['res.partner'].sudo().get_delivery_points()

#     def set_show_company(self, checkout, partner):
#         if partner.is_company:
#             checkout['show_company'] = True
#             checkout['company_name'] = partner.name
#         elif partner.parent_id:
#             checkout['show_company'] = True
#             checkout['company_name'] = partner.parent_id.name
#         else:
#             checkout['show_company'] = False
# 
#         return checkout

    def _get_mandatory_billing_fields(self):
        mandatory_billing_fields = super(WebsiteSale, self)._get_mandatory_billing_fields()
        if 'street2' in mandatory_billing_fields:
            mandatory_billing_fields.remove('street2')
        return mandatory_billing_fields

    def get_shipping_id(self, partner):
        if partner.raliment_point_id:
            return partner.raliment_point_id.id
        else:
            return partner.delivery_point_id.id

    def checkout_values(self):
        values = super(WebsiteSale, self).checkout_values()
        order = request.website.sale_get_order()
#        partner = order.partner_id

        #checkout = self.set_show_company(values.get('checkout'), partner)
#         if checkout.get('shipping_id') == False or checkout.get('shipping_id') in [-2,0]:
#             checkout['shipping_id'] = self.get_shipping_id(partner)
       # values['checkout'] = checkout
        values['shippings'] = self.get_delivery_points()
        return values

    @http.route(['/shop/cart/update'], 
                type='http',
                auth="public",
                methods=['POST'],
                website=True)
    def cart_update(self, product_id, add_qty=1, set_qty=0, **kw):
        try:
            super(WebsiteSale, self).cart_update(product_id, add_qty, set_qty,
                                                 **kw)
        except(UserError):
            request.redirect("/shop")
        return request.redirect("/shop/cart")

    @http.route(['/shop/cart/update_json'],
                type='json',
                auth="public",
                methods=['POST'],
                website=True)
    def cart_update_json(self, product_id, line_id=None, add_qty=None,
                         set_qty=None, display=True):
        try:
            value = super(WebsiteSale, self).cart_update_json(product_id,
                                                              line_id,
                                                              add_qty,
                                                              set_qty,
                                                              display)
        except(UserError):
            request.redirect("/shop")
        return value


class WebsiteAccount(CustomerPortal):

    @http.route(['/my/credit_account'], type='http',
                auth="user", website=True)
    def portal_my_credit_account(self, **kw):
        values = {
            'user_partner': request.env.user.partner_id,
        }
        return request.render("distribution_circuits_website_sale.credit_account", values)

    @http.route(['/my/account'], type='http', auth='user', website=True)
    def details(self, redirect=None, **post):
        partner = request.env['res.users'].browse(request.uid).partner_id
        values = {
            'error': {},
            'error_message': []
        }

        if post:
            error, error_message = self.details_form_validate(post)
            values.update({'error': error, 'error_message': error_message})
            values.update(post)
            if not error:
                post.update({'zip': post.pop('zipcode', '')})
                if partner.type == "contact":
                    address_fields = {
                        'city': post.pop('city'),
                        'street': post.pop('street'),
                        'zip': post.pop('zip'),
                        'country_id': post.pop('country_id'),
                        'state_id': post.pop('state_id')
                    }
                    partner.commercial_partner_id.sudo().write(address_fields)
                partner.sudo().write(post)
                if redirect:
                    return request.redirect(redirect)
                return request.redirect('/my/home')

        countries = request.env['res.country'].sudo().search([])
        states = request.env['res.country.state'].sudo().search([])

        values.update({
            'partner': partner,
            'countries': countries,
            'states': states,
            'has_check_vat': hasattr(request.env['res.partner'], 'check_vat'),
            'redirect': redirect,
        })

        return request.website.render("website_portal.details", values)

    def details_form_validate(self, data):
        error = dict()
        error_message = []

        mandatory_billing_fields = ["name", "phone", "email", "city",
                                    "country_id"]
        optional_billing_fields = ["zipcode", "company_name", "state_id",
                                   "vat", "street"]

        # Validation
        for field_name in mandatory_billing_fields:
            if not data.get(field_name):
                error[field_name] = 'missing'

        # email validation
        if data.get('email') and not tools.single_email_re.match(data.get('email')):
            error["email"] = 'error'
            error_message.append(_('Invalid Email! Please enter a valid email address.'))

        # vat validation
        if data.get("vat") and hasattr(request.env["res.partner"], "check_vat"):
            if request.website.company_id.vat_check_vies:
                # force full VIES online check
                check_func = request.env["res.partner"].vies_vat_check
            else:
                # quick and partial off-line checksum validation
                check_func = request.env["res.partner"].simple_vat_check
            vat_country, vat_number = request.env["res.partner"]._split_vat(data.get("vat"))
            if not check_func(vat_country, vat_number):  # simple_vat_check
                error["vat"] = 'error'
        # error message for empty required fields
        if [err for err in error.values() if err == 'missing']:
            error_message.append(_('Some required fields are empty.'))

        unknown = [k for k in data if k not in mandatory_billing_fields + optional_billing_fields]
        if unknown:
            error['common'] = 'Unknown field'
            error_message.append("Unknown field '%s'" % ','.join(unknown))

        return error, error_message


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
        values = dict((key, qcontext.get(key)) for key in ('login', 'name',
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
        request.env['res.partner.bank'].sudo().create(
            {'partner_id': user.partner_id.id, 'acc_number': iban})
        request.cr.commit()

    @http.route('/web/signup', type='http', auth='public', website=True)
    def web_auth_signup(self, *args, **kw):
        qcontext = self.get_auth_signup_qcontext()

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
                return super(AuthSignupHome, self).web_login(*args, **kw)
            except (SignupError, AssertionError) as e:
                if request.env["res.users"].sudo().search([
                        ("login", "=", qcontext.get("login"))]):
                    qcontext["error"] = _("Another user is already registered "
                                          "using this email address.")
                else:
                    _logger.error(e.message)
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
