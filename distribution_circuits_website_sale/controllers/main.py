# -*- coding: utf-8 -*-
# © 2016 Coop IT Easy (http://www.coopiteasy.be)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import logging

import datetime
from openerp import http
from openerp.http import request
from openerp import SUPERUSER_ID
from openerp.addons.website_sale.controllers.main import QueryURL
from openerp.tools.translate import _
from openerp.addons.website_sale.controllers.main import website_sale
from openerp.addons.website_portal_sale.controllers.main import website_account

_logger = logging.getLogger(__name__)

class WebsiteSale(website_sale):

    @http.route(['/shop',
                 '/shop/page/<int:page>',
                 '/shop/category/<model("product.public.category"):category>',
                 """/shop/category/<model("product.public.category"):category>
                 /page/<int:page>""",
                 '/shop/time_frame'],
                type='http',
                auth='user',
                website=True)
    def shop(self, page=0, category=None, time_frame=None, search='', **post):
        if time_frame:
            context = dict(request.env.context)
            context.setdefault('time_frame_id', int(time_frame))
            request.env.context = context
        return super(WebsiteSale, self).shop(page=page, category=category,
                                             time_frame=time_frame, search=search,
                                             **post)


    @http.route(['/shop/set_current_time_frame'], type='json', auth="public", methods=['POST'], website=True)
    def set_current_time_frame(self, time_frame_id=None, **kw):
        env  = request.env
        if time_frame_id :
            time_frame = env['time.frame'].sudo().browse(int(time_frame_id))
            request.session['selected_time_frame'] = time_frame.id
            return {time_frame.id: time_frame.name}
        else:
            request.session['selected_time_frame'] = None
        return {0:""}
    
    @http.route('/shop/payment/validate', type='http', auth="public", website=True)
    def payment_validate(self, transaction_id=None, sale_order_id=None, **post):
        if transaction_id is None:
            tx = request.website.sale_get_transaction()
        else:
            tx = request.env['payment.transaction'].sudo().browse(transaction_id)

        if sale_order_id is None:
            order = request.website.sale_get_order()
        else:
            order = request.env['sale.order'].sudo().browse(sale_order_id)
            assert order.id == request.session.get('sale_last_order_id')
        
        enough_credit = order.check_customer_credit()
        if enough_credit:
            tx.write({'state':'done'})
            return super(WebsiteSale, self).payment_validate(transaction_id, sale_order_id, **post)
        else:
            error = 'The customer credit is not sufficient to cover the payment %s set as error' % (tx.reference)
            _logger.info(error)
            return request.redirect('/shop')
    
    def get_delivery_points(self):
        return request.env['res.partner'].sudo().get_delivery_points()
    
    def set_show_company(self, checkout, partner):
        if partner.is_company:
            checkout['show_company'] = True
            checkout['company_name'] = partner.name
        elif partner.parent_id:
            checkout['show_company'] = True
            checkout['company_name'] = partner.parent_id.name
        else:
            checkout['show_company'] = False
        
        return checkout

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
        
    def checkout_values(self, data=None):
        values = super(WebsiteSale, self).checkout_values(data)
        order = request.website.sale_get_order()
        partner = order.partner_id
        
        checkout = self.set_show_company(values.get('checkout'), partner)
        if checkout.get('shipping_id') == False or checkout.get('shipping_id') in [-2,0]:
            checkout['shipping_id'] = self.get_shipping_id(partner)
        values['checkout'] = checkout
        values['shippings'] = self.get_delivery_points()
        return values

class WebsiteAccount(website_account):
    @http.route()
    def account(self, **kw):
        """ Add sales documents to main account page """
        response = super(WebsiteAccount, self).account()

        response.qcontext.update({
            'user_partner': request.env.user.partner_id,
        })
        return response
    
from openerp.addons.auth_signup.res_users import SignupError
from openerp.addons.auth_signup.controllers.main import AuthSignupHome

class AuthSignupHome(AuthSignupHome):    
    
    def do_signup(self, qcontext):
        """ Shared helper that creates a res.partner out of a token """
        values = dict((key, qcontext.get(key)) for key in ('login', 'name', 'password','phone','street','city','zip_code',
                                                           'country_id','raliment_point_id','delivery_point_id'))
        assert any([k for k in values.values()]), "The form was not properly filled in."
        assert values.get('password') == qcontext.get('confirm_password'), "Passwords do not match; please retype them."
        supported_langs = [lang['code'] for lang in request.env['res.lang'].sudo().search_read([], ['code'])]
        if request.lang in supported_langs:
            values['lang'] = request.lang
        values['zip'] = values['zip_code']
        qcontext['customer'] = True
        qcontext['need_validation'] = True
        self._signup_with_values(qcontext.get('token'), values)
        request.cr.commit()
    
    @http.route('/web/signup', type='http', auth='public', website=True)
    def web_auth_signup(self, *args, **kw):
        qcontext = self.get_auth_signup_qcontext()
        
        if not qcontext.get('raliment_point_id',False) and not qcontext.get('delivery_point_id',False):
            qcontext['error'] = _("You must at least choose a Raliment or a Delivery point")
        if qcontext.get('raliment_point_id',False) and qcontext.get('delivery_point_id',False):
            qcontext['error'] = _("You can not choose a Raliment and a Delivery point")
        
        if not qcontext.get('token') and not qcontext.get('signup_enabled'):
            raise werkzeug.exceptions.NotFound()

        if 'error' not in qcontext and request.httprequest.method == 'POST':
            try:
                self.do_signup(qcontext)
                return super(AuthSignupHome, self).web_login(*args, **kw)
            except (SignupError, AssertionError), e:
                if request.env["res.users"].sudo().search([("login", "=", qcontext.get("login"))]):
                    qcontext["error"] = _("Another user is already registered using this email address.")
                else:
                    _logger.error(e.message)
                    qcontext['error'] = _("Could not create a new account.")
        if not qcontext.get('raliment_point_id',False):
            qcontext['raliment_point_id'] = 0
        if not qcontext.get('delivery_point_id',False):
            qcontext['delivery_point_id'] = 0
        qcontext['raliment_points'] = request.env['res.partner'].sudo().get_raliment_points()
        qcontext['delivery_points'] = request.env['res.partner'].sudo().get_delivery_points()
        qcontext['countries'] = request.env['res.country'].sudo().search([])
        qcontext['country_id'] = '21'
        
        return request.render('auth_signup.signup', qcontext)
