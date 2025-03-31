This Odoo module automates the generation of XML IDs for product.template.attribute.value records. These records define the specific combinations of attributes and their values used to create product variants (e.g., "Color: Red, Size: Large").


## Functionality:

Automatic XML ID Generation:

The module overrides the create() method of the product.template.attribute.value model.
Whenever a new product.template.attribute.value record is created, the module automatically generates an XML ID for it.
XML ID Naming Convention:

The generated XML ID follows a predefined pattern, composed of the XML IDs of the related records:
prod_templ_id.xmlid: The XML ID of the associated product.template.
attribute_id.xmlid: The XML ID of the associated product.attribute.
attribute_value_id.xmlid: The XML ID of the associated product.attribute.value.

The parts are combined with underscorese.
This ensures that the XML ID is predictable and reflects the specific attribute value combination.

## Manual XML ID Generation:

The module also provides a method (generate_attribute_value_xmlids) that can be manually triggered to generate XML IDs for existing product.template.attribute.value records that might not have them.
Benefits:

Predictability: Ensures consistent and predictable XML IDs.
Automation: Automates the XML ID creation process.
Data Integrity: Maintains data integrity by generating unique XML IDs.
Integration: Simplifies integration with external systems.
