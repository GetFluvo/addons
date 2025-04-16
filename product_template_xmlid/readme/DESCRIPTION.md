This Odoo module automates the generation of XML IDs for product.template records. It is usefull in the scenario where a system, has been partially filled with the usu of odoo-data-flow.
odoo-data-flow import generally have an xmlid assigned.
When a user adds records trough the odoo UI. Generally no XMLID is generated.

This module allows to generate those XMLIDs automatically for those records.
This function can be triggered by:

- A cron job
- A button in the action menu of the product_template record.

## Functionality:

Automatic XML ID Generation:

* This module provides methods to automatically generate XML IDs for `product.template` records.
* It generates XML IDs for `product.template` records *after* they have been created using the `create()` method.
* XML IDs are only generated if they do not already exist, to ensure uniqueness.

This functionality is available for users in the group `erp_manager`.

**XML ID Naming Convention:**

* Generated XML IDs follow a defined pattern, constructed from the name of the `product.template` record.
    * The name is sanitized (spaces and other characters are replaced with underscores) to create a valid XML ID.
    * A predefined prefix (`_product`) is added to the sanitized name.
* This approach ensures predictable and contextually meaningful XML IDs.


## Manual XML ID Generation:

* The module provides a method (`generate_attribute_value_xmlids`) that can be manually invoked to generate XML IDs for existing `product.template` records that lack them.
* This is useful for batch generation or when initial data setup didn't include XML ID creation.


Predictability: Ensures consistent and predictable XML IDs.
Automation: Automates the XML ID creation process.
Data Integrity: Maintains data integrity by generating unique XML IDs.
Integration: Simplifies integration with external systems.
