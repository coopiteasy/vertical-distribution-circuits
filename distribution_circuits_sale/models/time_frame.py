# -*- coding: utf-8 -*-
from datetime import datetime

from openerp import api, fields, models, _

class TimeFrame(models.Model):
    
    _name = "time.frame"

    _order = "delivery_date, id"
        
    @api.onchange('delivery_date')
    def onchange_delivery_date(self):
        if self.delivery_date:
            self.name = datetime.strptime(self.delivery_date, "%Y-%m-%d").strftime('%A %d %B %Y')
    
    name = fields.Char(string="Time frame name")
    state = fields.Selection([('draft','Draft'),
                              ('validated','Validated'),
                              ('open','Open'),
                              ('cancel','Cancelled'),
                              ('closed','Closed'),
                              ('enclosed','Enclosed')], default="draft",string="State")
    start = fields.Datetime(string="Start", required=True)
    end = fields.Datetime(string="End", required=True)
    delivery_date = fields.Date(string="Delivery date", required=True)
    sale_orders = fields.One2many('sale.order','time_frame_id', string="Sale orders", readonly=True)
    
    @api.one
    def action_validate(self):
        self.write({'state':'validated'})
    
    @api.one
    def action_cancel(self):
        self.write({'state':'cancel'})
    
    @api.one
    def action_open(self):
        self.write({'state':'open'})
        
    @api.one
    def action_close(self):
        self.write({'state':'closed'})

    @api.one
    def action_draft(self):
        self.write({'state':'draft'})