# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRLfs
#     Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Website Sale Preset Carts",
    "summary": "Allows the sale manager to preset weekly carts",
    "version": "11.0.1.0.0",
    "category": "Sales",
    "website": "https://github.com/coopiteasy/vertical-distribution-circuits",
    "author": "Coop IT Easy SCRL fs",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "base",
        "distribution_circuits_base",
        "distribution_circuits_sale",
        "distribution_circuits_website_sale",
    ],
    "data": [
        "demo/demo.xml",
        "security/ir.model.access.csv",
        "views/res_partner.xml",
    ]
}
