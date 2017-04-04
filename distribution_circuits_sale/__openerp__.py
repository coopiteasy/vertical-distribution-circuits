# -*- coding: utf-8 -*-
##############################################################################
#
#    Coop IT Easy, Social Open Source Solution
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
    "name": "Short distribution circuits sale",
    "version": "1.0",
    "depends": ["distribution_circuits_base","sale"],
    "author": "Coop IT Easy - Houssine BAKKALI <houssine.bakkali@gmail.com>",
    "category": "Short distribution circuits",
    "description": """
    This module implements the features manage the sales of your distribution circuits.    
    """,
    'data': [
        'security/ir.model.access.csv',
        'views/menu_item.xml',
        'views/time_frame_view.xml',
        'views/sale_view.xml',
    ],
    'installable': True,
}