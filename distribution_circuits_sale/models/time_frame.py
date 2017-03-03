# -*- coding: utf-8 -*-
from datetime import datetime

from openerp import api, fields, models, _

class TimeFrame(models.Model):
    
    _name = "time.frame"
    
    @api.onchange('delivery_date')
    def onchange_delivery_date(self):
        if self.delivery_date:
            #self.name = _(datetime.strptime(self.delivery_date, "%Y-%m-%d").strftime('%A'))
            self.name = datetime.strptime(self.delivery_date, "%Y-%m-%d").strftime('%A %d %B %Y')
    
    name = fields.Char(string="Order closing date")
    start = fields.Datetime(string="Start", required=True)
    end = fields.Datetime(string="End", required=True)
    delivery_date = fields.Date(string="Delivery date", required=True)
    sale_orders = fields.One2many('sale.order','time_frame_id', string="Sale orders")
    state = fields.Selection([('draft','Draft'),
                              ('validated','Validated'),
                              ('open','Open'),
                              ('cancel','Cancelled'),
                              ('closed','Closed'),], string="State")
    