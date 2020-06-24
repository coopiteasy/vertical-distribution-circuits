# Copyright 2017 Coop IT Easy SCRLfs
#     Houssine Bakkali <houssine@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Short distribution circuits logistic",
    "version": "11.0.1.0.0",
    "depends": [
        "distribution_circuits_base",
        "distribution_circuits_sale",
        "sale_stock",
        "stock_picking_batch"],
    "author": "Coop IT Easy - Houssine BAKKALI <houssine@coopiteasy.be>",
    "licence": "AGPL-3",
    "website": "www.coopiteasy.be",
    "category": "Short distribution circuits",
    "description": """
    This module implements the features managing
    the sales of your distribution circuits.
    """,
    'data': [
        'security/ir.model.access.csv',
        'data/distribution_circuits_logistic_data.xml',
        'data/paperformat.xml',
        'views/menu_item.xml',
        'views/stock_view.xml',
        'views/delivery_round_view.xml',
        'views/picking_consolidation_view.xml',
        'views/time_frame_view.xml',
        # 'wizard/delivery_round_wizard.xml',
        # 'wizard/picking_consolidation_wizard.xml',
        'report/picking_consolidation_report.xml',
        'report/supplier_picking_consolidation_report.xml',
        'report/customer_picking_consolidation_report.xml',
        'report/logistic_report.xml',
    ],
    'installable': True,
}
