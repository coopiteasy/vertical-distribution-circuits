# Copyright 2017 Coop IT Easy SCRLfs
#     Houssine BAKKALI <houssine@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Short distribution circuits sale",
    'website': 'http://www.coopiteasy.be',
    'version': '11.0.1.0.1',
    'license': 'AGPL-3',
    "depends": [
        "product",
        "sale",
        "purchase",
        "distribution_circuits_base",
        "mail"
        ],
    "author": "Coop IT Easy SCRLfs",
    "licence": "AGPL-3",
    "website": "www.coopiteasy.be",
    "category": "Short distribution circuits",
    "description": """
    This module implements the features manage the sales
    of your distribution circuits.
    """,
    "demo": [
        'demo/demo.xml',
    ],
    'data': [
        'security/ir.model.access.csv',
        'report/sale_report_views.xml',
        'views/time_frame_view.xml',
        'views/sale_view.xml',
        'views/partner_view.xml',
        'views/purchase_view.xml',
        'views/sale_order_report_template.xml',
        'views/menu_item.xml',
    ],
    'installable': True,
}
