from odoo import models, fields, api
from odoo.http import request


class WebSite(models.Model):
    _inherit = 'website'

    current_time_frame = fields.Many2one(
        'time.frame',
        string='Selected time frame')

    # TODO refactor the code
    def get_current_time_frame(self):
        time_frame_ids = self.env['time.frame'].sudo().search([
            ('state', '=', 'open')]).ids
        if request.session.get('selected_time_frame'):
            session_time_frame = request.session.get('selected_time_frame')
            if session_time_frame in time_frame_ids:
                return session_time_frame
            elif len(time_frame_ids) > 0:
                request.session['selected_time_frame'] = time_frame_ids[0]
            else:
                request.session['selected_time_frame'] = None
        else:
            if len(time_frame_ids) > 0:
                request.session['selected_time_frame'] = time_frame_ids[0]
            else:
                request.session['selected_time_frame'] = None
        return request.session.get('selected_time_frame')

    @api.multi
    def get_open_time_frames(self):
        res = []
        for time_frame in self.env['time.frame'].sudo().search([
                ('state', '=', 'open')]):
            res.append((time_frame.id, time_frame.name))
        return res

    @api.multi
    def sale_get_order(self, force_create=False, code=None,
                       update_pricelist=False, force_pricelist=False,
                       context=None):
        sale_order = super(WebSite, self).sale_get_order(
            force_create=force_create, code=code,
            update_pricelist=update_pricelist, force_pricelist=force_pricelist,
            context=context)

        if sale_order and \
                (not sale_order.time_frame_id or \
                 sale_order.time_frame_id.state != 'open') \
                and request.session.get('selected_time_frame'):
            if sale_order.state == 'draft':
                sale_order.time_frame_id = int(request.session.get('selected_time_frame'))
        return sale_order

    @api.multi
    def sale_product_domain(self):
        domain = super(WebSite, self).sale_product_domain()
        # won't work
#         if 'time_frame_id' in self.env.context:
#             domain.append(
#                 ('time_frame_id', '=', self.env.context['time_frame_id']))
        return domain
