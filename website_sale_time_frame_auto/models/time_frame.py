# Copyright 2019 Coop IT Easy SCRLfs
#     Robin Keunen <robin@coopiteasy.be>
#     Manuel Claeys Bouuaert <manuel@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models
from datetime import datetime, timedelta
# from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as _format
import logging


_logger = logging.getLogger(__name__)


class TimeFrame(models.Model):
    _inherit = 'time.frame'

    @api.model
    def open_timeframes(self):
        now = datetime.now()
        last_hour = now - timedelta(hours=1)

        now_str = fields.Datetime.to_string(now)
        last_hour_str = fields.Datetime.to_string(last_hour)
        _logger.info('opening frames from %s to %s' % (last_hour_str, now_str))

        frames = self.search([
            ('state', '=', 'validated'),
            ('start', '>=', last_hour_str),
            ('start', '<=', now_str),
        ])
        _logger.info('opening frames %s' % frames)
        for frame in frames:
            _logger.info('opening frame %s' % frame.name)
            try:
                frame.action_open()
            except:
                if self.env['ir.config_parameter'].sudo().get_param(
                        'website_sale_time_frame_auto.send_mail_to_supervisor'):
                    email_template_timeframe_error_state = self.env.ref(
                        'website_sale_time_frame_auto.email_template_timeframe_error_state', False)
                    email_template_timeframe_error_state.sudo().send_mail(frame.id)

    @api.model
    def close_timeframes(self):
        now = datetime.now()
        last_hour = now - timedelta(hours=1)

        now_str = fields.Datetime.to_string(now)
        last_hour_str = fields.Datetime.to_string(last_hour)
        _logger.info('closing frames from %s to %s' % (last_hour_str, now_str))

        frames = self.search([
            ('state', '=', 'open'),
            ('end', '>=', last_hour_str),
            ('end', '<=', now_str),
        ])
        _logger.info('closing frames %s' % (frames))
        for frame in frames:
            _logger.info('closing frame %s' % frame.name)
            try:
                frame.action_close()
            except:
                if self.env['ir.config_parameter'].sudo().get_param(
                        'website_sale_time_frame_auto.send_mail_to_supervisor'):
                    email_template_timeframe_error_state = self.env.ref(
                        'website_sale_time_frame_auto.email_template_timeframe_error_state', False)
                    email_template_timeframe_error_state.sudo().send_mail(frame.id)

    @api.multi
    def action_open(self):
        self.ensure_one()
        res = super(TimeFrame, self).action_open()
        if self.env['ir.config_parameter'].sudo().get_param('website_sale_time_frame_auto.send_mail_to_supervisor'):
            email_template_timeframe_success_state = self.env.ref(
                'website_sale_time_frame_auto.email_template_timeframe_success_state', False)
            email_template_timeframe_success_state.sudo().send_mail(self.id)
        return res

    @api.multi
    def action_close(self):
        self.ensure_one()
        res = super(TimeFrame, self).action_close()
        if self.env['ir.config_parameter'].sudo().get_param('website_sale_time_frame_auto.send_mail_to_supervisor'):
            email_template_timeframe_success_state = self.env.ref(
                'website_sale_time_frame_auto.email_template_timeframe_success_state', False)
            email_template_timeframe_success_state.sudo().send_mail(self.id)
        return res
