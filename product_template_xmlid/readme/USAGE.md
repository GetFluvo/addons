# Usage Guide: `product_template_xmlid` Module

This document provides instructions on how to use the `product_template_xmlid` module in Odoo.

## Purpose

The `product_template_xmlid` module automates the generation of XML IDs for `product.template` records.


## Manual XML ID Generation

In some cases, you might have existing `product.template` records that were created manually and therefore lack XML IDs. The module provides a method to generate XML IDs for these records.

**Steps:**

1.  Navigate to the "Products" in the "Product" module.
2.  Open any form view of a `product.template` record.
3.  Click the gear icon (action menu) --> "Generate Product Template XML IDs" button.
4.  Odoo will generate XML IDs for all `product.template` records that currently don't have them.

## XML ID Naming Convention

The generated XML IDs follow this pattern:
PRODUCT_TEMPLATE.product_<productname>

**Example:**
PRODUCT_TEMPLATE.product_Pino

**Note:**

* Commas are replaced with underscores.
* Spaces are replaced with underscores.
* Dots are replaced with underscores.
* Pipes are replaced with underscores.
