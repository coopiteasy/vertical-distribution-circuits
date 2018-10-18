# -*- coding: utf-8 -*-

from odoo.exceptions import ValidationError
from odoo import models, api, fields
from odoo.tools.float_utils import float_compare
from odoo.tools.translate import _

import logging

_logger = logging.getLogger(__name__)


class PrepaidPaymentAcquirer(models.Model):
    _inherit = 'payment.acquirer'

    provider = fields.Selection(selection_add=[('prepaid', 'Prepaid')])

    @api.model
    def _get_providers(self):
        providers = super(PrepaidPaymentAcquirer, self)._get_providers()
        providers.append(['prepaid', _('Prepaid')])
        return providers

    @api.multi
    def prepaid_get_form_action_url(self):
        self.ensure_one()
        return '/payment/prepaid/feedback'


class PrepaidPaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    @api.model
    def _prepaid_form_get_tx_from_data(self, data):
        reference = data.get('reference')

        payment_tx = self.search([('reference', '=', reference)])
        if not payment_tx or len(payment_tx) > 1:
            error_msg = _('received data for reference %s') % (reference)
            if not payment_tx:
                error_msg += _('; no order found')
            else:
                error_msg += _('; multiple order found')
            _logger.error(error_msg)
            raise ValidationError(error_msg)

        return payment_tx

    def _prepaid_form_get_invalid_parameters(self, data):
        invalid_parameters = []

        if float_compare(float(data.get('amount', '0.0')), self.amount, 2) != 0:
            invalid_parameters.append(('amount', data.get('amount'), '%.2f' %
                                       self.amount))
        if data.get('currency') != self.currency_id.name:
            invalid_parameters.append(('currency', data.get('currency'),
                                       self.currency_id.name))

        return invalid_parameters

    def _prepaid_form_validate(self, data):
        _logger.info('Validated prepaid payment for tx %s: set as pending' %
                     (self.reference))
        return self.write({'state': 'pending'})
