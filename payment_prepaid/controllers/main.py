# -*- coding: utf-8 -*-
import logging
import pprint
import werkzeug

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class PrepaidController(http.Controller):
    _accept_url = '/payment/prepaid/feedback'

    @http.route([
        '/payment/prepaid/feedback',
    ], type='http', auth='none', csrf=False)
    def prepaid_form_feedback(self, **post):
        _logger.info('Beginning form_feedback with post data %s',
                     pprint.pformat(post))
        request.env['payment.transaction'].sudo().form_feedback(post, 'prepaid')
        return werkzeug.utils.redirect(post.pop('return_url', '/'))
