from odoo import fields, models


class SaleReport(models.Model):
    _inherit = "sale.report"

    raliment_point_id = fields.Many2one('res.partner', 'Point de Raliment', readonly=True)
    time_frame_id = fields.Many2one('time.frame', string="Time Frame", readonly=True)

    def _select(self):
        return super(SaleReport, self)._select() + ", partner.raliment_point_id as raliment_point_id, s.time_frame_id as time_frame_id"

    def _group_by(self):
        return super(SaleReport, self)._group_by() + ", partner.raliment_point_id, s.time_frame_id"
