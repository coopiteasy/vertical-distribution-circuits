# Copyright 2017 Coop IT Easy SCRLfs
#     Houssine Bakkali <houssine@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Distribution Circuits Website Registration',
    'category': 'e-commerce',
    'author': "Coop IT Easy - Houssine BAKKALI <houssine@coopiteasy.be>",
    'website': 'https://coopiteasy.be',
    'version': '11.0.1.0.0',
    'license': 'AGPL-3',
    'depends': [
                'distribution_circuits_website_sale',
                'portal',
                'website_sale',
                'auth_signup',
                ],
    "description": """
    This module allows to choose your raliment point preference and give
    complementary data during registration.
    """,
    'data': [
        "views/auth_signup_template.xml",
        "views/res_users_view.xml",
    ],
    'installable': True,
}
