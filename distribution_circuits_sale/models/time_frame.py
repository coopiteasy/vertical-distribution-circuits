from datetime import datetime

from odoo import api, fields, models


class TimeFrame(models.Model):
    _name = "time.frame"
    _order = "delivery_date, id"
    _inherit = ["mail.thread"]

    @api.onchange('delivery_date')
    def onchange_delivery_date(self):
        if self.delivery_date:
            self.name = datetime.strptime(
                self.delivery_date, "%Y-%m-%d").strftime('%A %d %B %Y')

    name = fields.Char(string="Time frame name")
    start = fields.Datetime(string="Start", required=True)
    end = fields.Datetime(string="End", required=True)
    delivery_date = fields.Date(string="Delivery date", required=True)
    filter_on_products = fields.Boolean(string="Activate filter on products")
    resellers_only = fields.Boolean(string="For resellers only")
    products = fields.Many2many('product.product', string='Products',
                                domain=[('sale_ok', '=', True),
                                        ('active', '=', True)])
    state = fields.Selection([('draft', 'Draft'),
                              ('validated', 'Validated'),
                              ('open', 'Open'),
                              ('cancel', 'Cancelled'),
                              ('closed', 'Closed'),
                              ('enclosed', 'Enclosed')],
                             default="draft",
                             string="State",
                             track_visibility="onchange")
    sale_orders = fields.One2many(
        'sale.order',
        'time_frame_id',
        string="Sale orders",
        readonly=True)

    purchase_orders = fields.One2many(
        'purchase.order',
        'time_frame_id',
        string="Purchase orders",
        readonly=True)

    @api.multi
    def action_validate(self):
        self.ensure_one()
        self.write({'state': 'validated'})

    @api.multi
    def action_cancel(self):
        self.ensure_one()
        self.write({'state': 'cancel'})

    @api.multi
    def action_open(self):
        self.ensure_one()
        self.write({'state': 'open'})

    @api.multi
    def action_close(self):
        self.ensure_one()
        self.write({'state': 'closed'})

    @api.multi
    def action_enclose(self):
        self.ensure_one()
        self.write({'state': 'enclosed'})

    @api.multi
    def action_draft(self):
        self.ensure_one()
        self.write({'state': 'draft'})
