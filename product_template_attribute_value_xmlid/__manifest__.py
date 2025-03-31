# -*- coding: utf-8 -*-
# Copyright 2025 Odoo Data Flow
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    'name': 'Generate XML IDs for Product Template Attribute Values',
    'version': '18.0.1.0.0',
    'summary': 'Generates predictable XML IDs for product.template.attribute.value records based on template and attribute values. These can be used to generate predictable combinations for product.product records.',
    'description': 'This module generates XML IDs for product.template.attribute.value records after importing product.template.attribute.line.',
    'author': 'Odoo Data Flow',
    'website': 'https://github.com/OdooDataFlow/addons',
    'category': 'Technical Settings',
    'version': '18.0.1.0.0',
    'depends': [
        'product',
        'sale_management',

    ],
    # 'excludes': ['product_barcodelookup',],
    'data': ['views/product_template_attribute_view.xml'],
    'license': 'LGPL-3',
    'installable': True,
    'cloc_exclude': [
    ]
}
