# Copyright 2018 Coop IT Easy SCRLfs
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "eCommerce - Filter Products by Suppliers",
    "summary": "Let the user filter products by suppliers in the e-commerce.",
    "version": "11.0.1.0.0",
    # see https://odoo-community.org/page/development-status
    "development_status": "Alpha",
    "category": "eCommerce",
    "website": "https://github.com/houssine78/vertical-distribution-circuits",
    "author": "Coop IT Easy SCRLfs",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "website_sale",
    ],
    "data": [
        "views/filter_template.xml",
    ],
}
