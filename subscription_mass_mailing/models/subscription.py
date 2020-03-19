# Copyright 2019 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
#   Houssine Bakkali <houssine@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, api


class Subscription(models.Model):
    _inherit = "subscription"

    @api.multi
    def message_get_default_recipients(self):
        self.ensure_one()
        return {
            self.id: {
                "partner_ids": [subscriber.id],
                "email_to": subscriber.email,
                "email_cc": False,
            }
            for subscriber in self.subscriber_ids
        }
