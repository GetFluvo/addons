# Usage Guide: `product_template_attribute_value_xmlid` Module

This document provides instructions on how to use the `product_template_attribute_value_xmlid` module in Odoo.

## Purpose

The `product_template_attribute_value_xmlid` module automates the generation of XML IDs for `product.template.attribute.value` records, which represent specific combinations of product attributes and their values. This is crucial for data integration and automation purposes.


## Automatic XML ID Generation

Once installed, the module automatically generates XML IDs for new `product.template.attribute.value` records. You don't need to perform any manual steps for this.

**Example:**

When you create a new product template with attributes (e.g., Color: Red, Size: Large), the corresponding `product.template.attribute.value` records created by Odoo will automatically receive XML IDs.

## Manual XML ID Generation (Optional)

In some cases, you might have existing `product.template.attribute.value` records that were created before installing this module and therefore lack XML IDs. The module provides a method to generate XML IDs for these records.

**Steps:**

1.  Navigate to the "Product Attribute Values" in the "Product" module.
2.  Open any form view of a `product.template.attribute.value` record.
3.  Click the "Generate XML IDs" button.
4.  Odoo will generate XML IDs for all `product.template.attribute.value` records that currently don't have them.

## XML ID Naming Convention

The generated XML IDs follow this pattern:
prod_templ_<product_template_xmlid>_attr_<attribute_xmlid>_val_<attribute_value_xmlid>

**Example:**
prod_templ_product_template_123_attr_color_val_red

* `prod_templ_`: Prefix indicating "product template."
* `<product_template_xmlid>`: The XML ID of the related `product.template` record.
* `attr_`: Prefix indicating "attribute."
* `<attribute_xmlid>`: The XML ID of the related `product.attribute` record.
* `val_`: Prefix indicating "attribute value."
* `<attribute_value_xmlid>`: The XML ID of the related `product.attribute.value` record.

**Note:**

* All parts of the XML ID are converted to lowercase.
* Spaces are replaced with underscores.

## Important Considerations

* Ensure that the related `product.template`, `product.attribute`, and `product.attribute.value` records have XML IDs for the automatic generation to work correctly.
* The module aims to generate unique XML IDs. However, if you have existing data with conflicting names or IDs, you might need to resolve those conflicts manually.
