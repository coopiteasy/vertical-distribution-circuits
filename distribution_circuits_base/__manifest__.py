# -*- coding: utf-8 -*-
##############################################################################
#
#    OAC, Business Open Source Solution
#    Copyright (C) 2017-2017 Coop IT Easy.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    "name": "Short distribution circuits base",
    "version": "11.0.1.0.0",
    "depends": [
            "base",
            "purchase",
            "partner_firstname"
    ],
    "author": "Coop IT Easy - Houssine BAKKALI <houssine@coopiteasy.be>",
    "licence": "AGPL-3",
    "website": "www.coopiteasy.be",
    "category": "Short distribution circuits",
    "description": """
    This module give the base features to enable the
    short distribution circuits.
    """,
    'data': [
        'security/easy_my_hub_security.xml',
        'views/menu_item.xml',
        'views/res_partner_view.xml',
    ],
    'installable': True,
    'application': True,
}
