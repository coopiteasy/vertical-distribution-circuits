# Copyright 2019 Coop IT Easy SCRLfs
#     Robin Keunen <robin@coopiteasy.be>
#     Manuel Claeys Bouuaert <manuel@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Website Sale Time Frame Automatic Open/Close",
    "summary": """
        Allows automatic open/close of fime frames using cron scheduled actions. 
        Option to send email to supervisor on successful opening or closing,
        and failed scheduled opening or closing. 
    """,
    "version": "11.0.1.0.0",
    "category": "Sales",
    "website": "https://coopiteasy.be",
    "author": "Coop IT Easy SCRL fs",
    "license": "AGPL-3",
    "depends": [
        "base",
        "dc_website_registration",
        "distribution_circuits_base",
        "distribution_circuits_sale",
        "distribution_circuits_website_sale",
    ],
    "data": [
        "data/cron.xml",
        "data/mail_template.xml",
        "views/res_config_settings.xml",
    ],
    "installable": True
}
