# Copyright 2019 Coop IT Easy SCRLfs
#     Robin Keunen <robin@coopiteasy.be>
#     Houssine Bakkali <houssine@coopiteasy.be>
#     Manuel Claeys Bouuaert <manuel@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Website Sale Preset Carts",
    "summary": "Allows the sale manager to preset weekly carts",
    "version": "11.0.2.0.2",
    "category": "Sales",
    "website": "https://www.coopiteasy.be",
    "author": "Coop IT Easy SCRL fs",
    "license": "AGPL-3",
    "depends": [
        "base",
        "dc_website_registration",
        "distribution_circuits_base",
        "distribution_circuits_sale",
        "distribution_circuits_website_sale",
    ],
    "demo": [
        "demo/demo.xml",  # fixme
    ],
    "data": [
        "data/cron.xml",
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
    ],
    "installable": True
}
