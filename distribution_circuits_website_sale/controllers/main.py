# -*- coding: utf-8 -*-
# © 2016 Coop IT Easy (http://www.coopiteasy.be)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import logging

import datetime
from openerp import http
from openerp.http import request
from openerp import SUPERUSER_ID
from openerp.addons.website_sale.controllers.main import QueryURL
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
    
#     def check_customer_credit(self, order):
#         partner = order.partner_id
#         if partner.credit - partner.amount_due - order.amount_total >= order.amount_total:
#             return True
#         else:
#             return False
    
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
        

class WebsiteAccount(website_account):
    @http.route()
    def account(self, **kw):
        """ Add sales documents to main account page """
        response = super(WebsiteAccount, self).account()

        response.qcontext.update({
            'user_partner': request.env.user.partner_id,
        })
        return response