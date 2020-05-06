# Copyright 2019 Coop IT Easy SCRLfs
#     Robin Keunen <robin@coopiteasy.be>
#     Houssine Bakkali <houssine@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Website Sale Preset Carts",
    "summary": "Allows the sale manager to preset weekly carts",
    "version": "11.0.2.0.0",
    "category": "Sales",
    "website": "https://github.com/coopiteasy/vertical-distribution-circuits",
    "author": "Coop IT Easy SCRL fs",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "base",
        "distribution_circuits_base",
        "distribution_circuits_sale",
        "distribution_circuits_website_sale",
        "dc_website_registration",
    ],
    "demo": [
        "demo/demo.xml",  # fixme
    ],
    "data": [
        "data/cron.xml",
        "data/res_config_settings.xml",
        "security/ir.model.access.csv",
        "views/auth_signup_template.xml",
        "views/preset_cart.xml",
        "views/res_config_settings.xml",
        "views/res_partner.xml",
        "views/time_frame.xml",
        "views/subscription.xml",
        "views/menu.xml",
        "templates/suspend_cart_portal.xml",
        "templates/suspend_cart_form.xml",
    ]
}
