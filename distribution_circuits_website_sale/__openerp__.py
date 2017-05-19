# -*- coding: utf-8 -*-
# © 2017 Coop IT Easy (http://www.coopiteasy.be)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Distribution Circuits in E-Commerce',
    'category': 'e-commerce',
    'author': "Coop IT Easy - Houssine BAKKALI",
    'website': 'http://www.coopiteasy.be',
    'version': '9.0.1.0.0',
    'license': 'AGPL-3',
    'depends': ['distribution_circuits_sale',
                'website_sale',
                'website_portal_sale',
                'website_payment',
                'auth_signup'
    ],
    'data': [
        "security/ir.model.access.csv",
      #  "data/website_menu.xml",
        "views/website_sale_template.xml",
        "views/website_portal_sale_template.xml",
        "views/auth_signup_template.xml",
        "views/res_users_view.xml",
    ],
    'installable': True,
}
