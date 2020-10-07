# Copyright 2020 Coop IT Easy SCRLfs
#     Houssine Bakkali <houssine@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Website Sale Preset Carts Signup",
    "summary": "Glue module to add fields to registration page",
    "version": "11.0.1.0.1",
    "category": "Sales",
    "website": "https://www.coopiteasy.be",
    "author": "Coop IT Easy SCRL fs",
    "license": "AGPL-3",
    "depends": [
        "dc_website_registration",
        "website_sale_preset_carts",
    ],
    "data": [
        "views/auth_signup_template.xml",
    ],
    "installable": True,
    "auto_install": True
}
