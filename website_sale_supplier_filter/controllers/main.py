# Copyright 2018 Coop IT Easy SCRLfs
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import datetime
from werkzeug.exceptions import NotFound

from odoo import http
from odoo.http import request
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.distribution_circuits_website_sale.controllers.main import WebsiteSale as Base


class WebsiteSale(Base):

    def _get_search_domain(self, search, category, attrib_values):
        domain = super()._get_search_domain(search, category, attrib_values)
        if 'filter_supplier_id' in request.env.context:
            supplier = request.env.context['filter_supplier_id']
            sellers = request.env['product.supplierinfo'].sudo().search([
                ('name', 'child_of', int(supplier)),
                '|', ('date_start', '<=', datetime.today()),
                ('date_start', '=', None),
                '|', ('date_end', '>=', datetime.today()),
                ('date_end', '=', None),
            ])
            domain.append(
                ('seller_ids', 'in', sellers.ids)
            )
        return domain

    @http.route()
    def shop(self, page=0, category=None, supplier=None, search='', ppg=False,
             **post):
        res_partner_mgr = request.env['res.partner']

        if supplier:
            supplier = res_partner_mgr.browse(int(supplier))
            if not supplier:
                raise NotFound()

        # Put supplier in the context so that it is accessible by other
        # function of this controller.
        if supplier:
            context = dict(request.env.context)
            context['filter_supplier_id'] = supplier
            request.env.context = context

        response = super().shop(page=page, category=category, search=search, ppg=ppg, **post)

        # Build the new `keep` function to keep arguments in the URL
        attrib_list = request.httprequest.args.getlist('attrib')
        keep = QueryURL('/shop', category=category and int(category),
                        search=search, attrib=attrib_list,
                        supplier=supplier and int(supplier),
                        order=post.get('order'))

        # Add element to context
        response.qcontext['keep'] = keep
        response.qcontext['supplier'] = supplier
        response.qcontext['suppliers'] = res_partner_mgr.sudo().search([
            ('supplier', '=', True)
        ])

        return response
