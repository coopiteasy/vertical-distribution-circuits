# Copyright 2019 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
#   Houssine Bakkali <houssine@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Subscription - Mass Mailing",
    "version": "12.0.1.0.0",
    "description": "Define criteria to send email to subscribers",
    "category": "Short distribution circuits",
    "author": "Coop IT Easy SCRL",
    "website": "www.coopiteasy.be",
    "license": "AGPL-3",
    "depends": ["mail", "mass_mailing", "website_sale_preset_carts"],
    "data": [
        "security/ir.model.access.csv",
        "views/mailing_criterium_view.xml",
        "data/cron.xml",
    ],
    "demo": [],
    "installable": True,
}
