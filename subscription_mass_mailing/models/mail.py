# Copyright 2019 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
#   Houssine Bakkali <houssine@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class Mail(models.Model):
    _inherit = "mail.mail"

    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Subscriber"
    )
    criterium_id = fields.Many2one(
        comodel_name="ps.mailing.criterium",
        string="Criterium"
    )
    mail_template_id = fields.Many2one(
        comodel_name="mail.template",
        string="Email Template",
        related="criterium_id.mail_template",
    )
