# -*- coding: utf-8 -*-

from openerp.addons.payment.models.payment_acquirer import ValidationError
from openerp import models, fields, api
from openerp.tools.float_utils import float_compare
from openerp.tools.translate import _

import logging
import pprint

_logger = logging.getLogger(__name__)


class PrepaidPaymentAcquirer(models.Model):
    _inherit = 'payment.acquirer'

    @api.model
    def _get_providers(self):
        providers = super(PrepaidPaymentAcquirer, self)._get_providers()
        providers.append(['prepaid', _('Prepaid')])
        return providers

    @api.multi
    def prepaid_get_form_action_url(self):
        self.ensure_one()
        return '/payment/prepaid/feedback'

#     def _format_transfer_data(self, cr, uid, context=None):
#         company_id = self.pool['res.users'].browse(cr, uid, uid, context=context).company_id.id
#         # filter only bank accounts marked as visible
#         journal_ids = self.pool['account.journal'].search(cr, uid, [('type', '=', 'bank'), ('display_on_footer', '=', True), ('company_id', '=', company_id)], context=context)
#         accounts = self.pool['account.journal'].browse(cr, uid, journal_ids, context=context).mapped('bank_account_id').name_get()
#         bank_title = _('Bank Accounts') if len(accounts) > 1 else _('Bank Account')
#         bank_accounts = ''.join(['<ul>'] + ['<li>%s</li>' % name for id, name in accounts] + ['</ul>'])
#         post_msg = _('''<div>
# <h3>Please use the following transfer details</h3>
# <h4>%(bank_title)s</h4>
# %(bank_accounts)s
# <h4>Communication</h4>
# <p>Please use the order name as communication reference.</p>
# </div>''') % {
#             'bank_title': bank_title,
#             'bank_accounts': bank_accounts,
#         }
#         return post_msg
# 
#     def create(self, cr, uid, values, context=None):
#         """ Hook in create to create a default post_msg. This is done in create
#         to have access to the name and other creation values. If no post_msg
#         or a void post_msg is given at creation, generate a default one. """
#         if values.get('provider') == 'prepaid' and not values.get('post_msg'):
#             values['post_msg'] = self._format_transfer_data(cr, uid, context=context)
#         return super(TransferPaymentAcquirer, self).create(cr, uid, values, context=context)


class PrepaidPaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    @api.model
    def _prepaid_form_get_tx_from_data(self, data):
        reference, amount, currency_name = data.get('reference'), data.get('amount'), data.get('currency_name')
        
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
    
    @api.model
    def _prepaid_form_get_invalid_parameters(self, tx, data):
        invalid_parameters = []

        if float_compare(float(data.get('amount', '0.0')), tx.amount, 2) != 0:
            invalid_parameters.append(('amount', data.get('amount'), '%.2f' % tx.amount))
        if data.get('currency') != tx.currency_id.name:
            invalid_parameters.append(('currency', data.get('currency'), tx.currency_id.name))
#         if tx.partner_reference and data.get('customerId') != tx.partner_reference:
#             invalid_parameters.append(('customerId', data.get('customerId'), tx.partner_reference))
            
        return invalid_parameters
    
    @api.model
    def _prepaid_form_validate(self, tx, data):
        """
        handle the different cases here or just manage them in another model?
        """
        _logger.info('Validated prepaid payment for tx %s: set as pending' % (tx.reference))
        return tx.write({'state': 'pending'})
