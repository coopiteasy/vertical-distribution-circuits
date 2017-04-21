# -*- coding: utf-8 -*-
import logging
import pprint
import werkzeug

from openerp import http, SUPERUSER_ID
from openerp.http import request

_logger = logging.getLogger(__name__)


class PrepaidController(http.Controller):
    _accept_url = '/payment/prepaid/feedback'

    @http.route([
        '/payment/prepaid/feedback',
    ], type='http', auth='none', csrf=False)
    def prepaid_form_feedback(self, **post):
        cr, uid, context = request.cr, SUPERUSER_ID, request.context
        _logger.info('Beginning form_feedback with post data %s', pprint.pformat(post))  # debug
        request.registry['payment.transaction'].form_feedback(cr, uid, post, 'prepaid', context)
        return werkzeug.utils.redirect(post.pop('return_url', '/'))
