# Product Template Attribute Lines Menu

This Odoo module enhances the user interface by providing a dedicated menu item for managing `product.template.attribute.line` records. This improves accessibility and streamlines workflows related to product attribute configuration.

## Features

* **Dedicated Menu Item:**
    * Adds a new menu item labeled "Product Template Attribute Lines."
    * This menu item is located under **Sales > Configuration > Products**, providing a clear and logical placement for users working with product attributes.

* **Direct Access to List View:**
    * The menu item opens a list view of the `product.template.attribute.line` model.
    * This allows users to quickly view, search, and manage existing attribute lines.

* **Enabled Record Creation:**
    * The module overrides the default tree view of `product.template.attribute.line` to enable the creation of new records directly from the list view.
    * This simplifies the process of adding new attribute lines, especially when importing data or configuring products.

## Benefits

* **Improved User Experience:** Provides a more intuitive and efficient way to access and manage product template attribute lines.
* **Streamlined Workflows:** Reduces the number of clicks and navigation steps required for common attribute configuration tasks.
* **Simplified Data Import:** Facilitates the import of `product.template.attribute.line` data by enabling direct creation of records from the list view.

## Usage

After installing the module, navigate to **Sales > Configuration > Products** to find the new "Product Template Attribute Lines" menu item.

## Technical Details

* The module defines an `ir.actions.act_window` action to open the list view of `product.template.attribute.line`.
* It overrides the default tree view of `product.template.attribute.line` to set the `create` attribute to "1", enabling record creation.
