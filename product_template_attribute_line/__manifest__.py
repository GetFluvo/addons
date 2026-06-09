# Copyright 2025 Fluvo
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    "name": "Product Template Attribute Lines Menu",
    "version": "18.0.1.0.0",
    "summary": "Adds a menu item for product.template.attribute.line",
    "author": "Fluvo",
    "website": "https://github.com/GetFluvo/addons",
    "category": "Technical Settings",
    "depends": [
        "product",
        # 'sale_management',
    ],
    # 'excludes': ['product_barcodelookup',],
    "data": [
        "views/product_template_attribute_line_views.xml",
    ],
    "license": "LGPL-3",
    "installable": True,
    "cloc_exclude": [],
}
