# Copyright 2017 Coop IT Easy SCRLfs
#     Houssine Bakkali <houssine@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Distribution Circuits in E-Commerce',
    'category': 'e-commerce',
    'author': "Coop IT Easy - Houssine BAKKALI <houssine@coopiteasy.be>",
    'website': 'https://coopiteasy.be',
    'version': '11.0.2.0.0',
    'license': 'AGPL-3',
    'depends': ['distribution_circuits_base',
                'distribution_circuits_sale',
                'portal',
                'website_sale',
                'website_payment',
                'mail',
                ],
    "description": """
    This module implements the e-commerce features manage the sales
    of your distribution circuits.
    """,
    'data': [
        "data/cron.xml",
        "data/mail_templates.xml",
        "security/ir.model.access.csv",
        "views/website_sale_template.xml",
        "views/website_portal_sale_template.xml",
        "views/res_config_settings_views.xml",
    ],
    'installable': True,
}
