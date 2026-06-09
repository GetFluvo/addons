# Copyright 2025 Fluvo
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    "name": "Generate XML IDs for Product Template Attribute Values",
    "version": "18.0.1.0.0",
    "summary": (
        "Generates predictable XML IDs for "
        "product.template.attribute.value records based on template "
        "and attribute values. These can be used to generate predictable "
        "combinations for product.product records."
    ),
    "author": "Fluvo",
    "website": "https://github.com/GetFluvo/addons",
    "category": "Technical Settings",
    "depends": [
        "product",
        "sale_management",
    ],
    # 'excludes': ['product_barcodelookup',],
    "data": ["views/product_template_attribute_view.xml"],
    "license": "LGPL-3",
    "installable": True,
    "cloc_exclude": [],
}
