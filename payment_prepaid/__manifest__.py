# -*- coding: utf-8 -*-
# © 2017 Coop IT Easy (http://www.coopiteasy.be)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Prepaid Payment Acquirer',
    'category': 'Accounting',
    'summary': 'Payment Acquirer: Prepaid Implementation',
    'author': "Coop IT Easy - Houssine BAKKALI <houssine@coopiteasy.be",
    'website': 'http://www.coopiteasy.be',
    'version': '11.0.1.0.0',
    'license': 'AGPL-3',
    'description': """Prepaid Payment Acquirer""",
    'depends': ['payment'],
    'data': [
        'views/prepaid.xml',
        'data/prepaid.xml',
    ],
    'installable': True,
}
