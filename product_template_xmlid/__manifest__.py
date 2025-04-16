# Copyright 2025 Odoo Data Flow
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    "name": "Generate XML IDs for Product Template",
    "version": "18.0.1.0.0",
    "summary": (
        "Generates predictable XML IDs for "
        "product.template records "
        "It is usefull if a set have an xmlid assigned to them by a product import. "
        "You want to use the same xmlid structure for records generated from the ui "
    ),
    "author": "Odoo Data Flow",
    "website": "https://github.com/OdooDataFlow/addons",
    "category": "Technical Settings",
    "depends": [
        "product",
        "sale_management",
    ],
    "excludes": [],
    "data": [
        "security/ir.model.access.csv",
        "wizard/generate_wizard_view.xml",
        "data/ir_cron.xml",
    ],
    "license": "LGPL-3",
    "installable": True,
    "cloc_exclude": [],
}
