import logging

from odoo import http
from odoo.http import request
from odoo.tools.translate import _
from odoo import tools
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.portal.controllers.portal import CustomerPortal

from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class WebsiteSale(WebsiteSale):

    def _get_search_domain(self, search, category, attrib_values):
        domain = super(WebsiteSale, self)._get_search_domain(search, category,
                                                             attrib_values)
        time_frame_obj = request.env['time.frame']
        tf_id = request.website.get_current_time_frame()
        if tf_id:
            time_frame = time_frame_obj.sudo().browse(tf_id)
            if time_frame.filter_on_products:
                domain.append(
                    ('id', 'in', time_frame.products.mapped('product_tmpl_id.id')))
        return domain

    @http.route([
        '/shop',
        '/shop/page/<int:page>',
        '/shop/category/<model("product.public.category"):category>',
        '/shop/category/<model("product.public.category"):category>/page/<int:page>',  # noqa
    ], type='http', auth='user', website=True)
    def shop(self, page=0, category=None, time_frame=None, search='', **post):
        time_frames = request.website.get_open_time_frames()
        if len(time_frames) == 0:
            return request.render(
                "distribution_circuits_website_sale.shop_closed", post)
        else:
            values = super(WebsiteSale, self).shop(page=page,
                                                   category=category,
                                                   time_frame=time_frame,
                                                   search=search,
                                                   **post)
            return values

    @http.route(['/shop/set_current_time_frame'],
                type='json',
                auth="public",
                methods=['POST'],
                website=True)
    def set_current_time_frame(self, time_frame_id=None, **kw):
        tf_obj = request.env['time.frame']
        if time_frame_id:
            time_frame = tf_obj.sudo().browse(int(time_frame_id))
            if request.website.sale_get_order():
                order = request.website.sale_get_order()
                request.session['selected_time_frame'] = time_frame.id

                # don't update the time frame on the sale order and invalidate
                # the cart(sale order) if it's not in draft state
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
            else:
                request.session['selected_time_frame'] = time_frame.id
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
            tx = request.env['payment.transaction'].browse(transaction_id)

        if sale_order_id is None:
            order = request.website.sale_get_order()
        else:
            order = request.env['sale.order'].sudo().browse(sale_order_id)
            assert order.id == request.session.get('sale_last_order_id')

        if not order or (order.amount_total and not tx):
            return request.redirect('/shop')

        if order.payment_acquirer_id.provider == "prepaid":
            if order.check_customer_credit():
                if tx:
                    tx.write({'state': 'done'})
                    order.with_context(send_email=True).action_confirm()
                    return request.redirect('/shop/confirmation')
            else:
                _logger.error('The customer credit is not sufficient to cover'
                              'the payment %s set as error' % (tx.reference))
                return request.redirect('/shop')
        else:
            return super(WebsiteSale, self).payment_validate(transaction_id,
                                                             sale_order_id,
                                                             **post)

    def get_delivery_points(self):
        return request.env['res.partner'].sudo().get_delivery_points()

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
        env = request.env
        partner = env.user.partner_id
        move_lines = env['account.move.line'].sudo().search(
            [('partner_id', '=', partner.id),
             ('account_id', '=', partner.property_account_receivable_id.id)]
            )
        values = {
            'user_partner': partner,
            'move_lines': move_lines,
        }
        return request.render("distribution_circuits_website_sale.credit_account", values)

    @http.route(['/my/account'], type='http', auth='user', website=True)
    def details(self, redirect=None, **post):
        partner = request.env.user.partner_id
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
