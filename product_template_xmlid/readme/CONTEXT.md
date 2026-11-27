Products created in the interface get no XML ID. Imports and integrations then
have to reference them by database id, which differs between databases, or by
name, which is not unique.

`product_template_attribute_value_xmlid` only names the attribute values of
products that have an XML ID, so the variants of these products could not be
referenced either.
