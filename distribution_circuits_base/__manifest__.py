# Copyright 2017 Coop IT Easy SCRLfs
#     Houssine Bakkali <houssine@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Short distribution circuits base",
    "version": "11.0.1.0.0",
    "depends": [
            "base",
            "purchase",
            "partner_firstname"
    ],
    "author": "Coop IT Easy - Houssine BAKKALI <houssine@coopiteasy.be>",
    "license": "AGPL-3",
    "website": "www.coopiteasy.be",
    "category": "Short distribution circuits",
    "description": """
    This module give the base features to enable the
    short distribution circuits.
    """,
    "demo": [
        'demo/demo.xml',
    ],
    'data': [
        'security/easy_my_hub_security.xml',
        'views/res_partner_view.xml',
        'views/menu_item.xml',
    ],
    'installable': True,
    'application': True,
}
