import logging
from odoo import fields, models

_logger = logging.getLogger(__name__)


class PurchaseOrder(models.Model):

    _inherit = "purchase.order"

    time_frame_id = fields.Many2one('time.frame', string="Time Frame")
