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
        selected_tf = request.session.get('selected_time_frame')
        if request.session.get('selected_time_frame'):
            if selected_tf in time_frame_ids:
                return selected_tf
            elif len(time_frame_ids) > 0:
                selected_tf = time_frame_ids[0]
            else:
                selected_tf = None
        else:
            order = self.sale_get_order()
            if len(time_frame_ids) > 0:
                if order:
                    selected_tf = order.time_frame_id.id
                else:
                    selected_tf = time_frame_ids[0]
            else:
                selected_tf = None

        request.session['selected_time_frame'] = selected_tf

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
                       update_pricelist=False, force_pricelist=False):
        sale_order = super(WebSite, self).sale_get_order(
            force_create=force_create, code=code,
            update_pricelist=update_pricelist, force_pricelist=force_pricelist)

        if sale_order and \
                (not sale_order.time_frame_id or
                 sale_order.time_frame_id.state != 'open') \
                and request.session.get('selected_time_frame'):
            if sale_order.state == 'draft':
                sale_order.time_frame_id = int(request.session.get('selected_time_frame'))
        return sale_order
