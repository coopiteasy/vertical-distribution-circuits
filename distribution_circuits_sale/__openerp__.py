# -*- coding: utf-8 -*-
# © 2017 Coop IT Easy (http://www.coopiteasy.be)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Short distribution circuits sale",
    'website': 'http://www.coopiteasy.be',
    'version': '9.0.1.0.0',
    'license': 'AGPL-3',
    "depends": [
        "product",
        "sale",
        "purchase",
        "distribution_circuits_base"
        ],
    "author": "Coop IT Easy - Houssine BAKKALI <houssine@coopiteasy.be>",
    "licence": "AGPLv3",
    "website": "www.coopiteasy.be",
    "category": "Short distribution circuits",
    "description": """
    This module implements the features manage the sales
    of your distribution circuits.
    """,
    'data': [
        'security/ir.model.access.csv',
        'views/menu_item.xml',
        'views/time_frame_view.xml',
        'views/sale_view.xml',
        'views/partner_view.xml',
        'views/sale_order_report_template.xml'
    ],
    'installable': True,
}
