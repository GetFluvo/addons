# -*- coding: utf-8 -*-
# Copyright 2025 Odoo Data Flow
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    'name': 'Product Template Attribute Lines Menu',
    'version': '18.0',
    'summary': 'Adds a menu item for product.template.attribute.line',
    'author': 'Odoo Data Flow',
    'website': 'https://github.com/OdooDataFlow/addons',
    'category': 'Technical Settings',
    'version': '18.0.1.0.0',
    'depends': [
        'product',
        # 'sale_management',

    ],
    # 'excludes': ['product_barcodelookup',],
    'data': ['views/product_template_attribute_line_views.xml',],
    'license': 'LGPL-3',
    'installable': True,
    'cloc_exclude': [
    ]
}
