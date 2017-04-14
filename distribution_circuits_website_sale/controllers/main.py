# -*- coding: utf-8 -*-
# © 2016 Coop IT Easy (http://www.coopiteasy.be)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import http
from openerp.http import request
from openerp import SUPERUSER_ID
from openerp.addons.website_sale.controllers.main import QueryURL
from openerp.addons.website_sale.controllers.main import website_sale


class WebsiteSale(website_sale):

    @http.route(['/shop',
                 '/shop/page/<int:page>',
                 '/shop/category/<model("product.public.category"):category>',
                 """/shop/category/<model("product.public.category"):category>
                 /page/<int:page>""",
                 '/shop/time_frame'],
                type='http',
                auth='public',
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