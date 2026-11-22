This module gives every `product.template.attribute.value` record a predictable
XML ID, so that product variants can be referenced in imports and integrations
without looking up database ids.

When Odoo creates a template attribute value, the module adds an XML ID
`product_template_attribute_value.<template>_<value>`, where:

- `<template>` is the name of the XML ID of the product template;
- `<value>` is the name of the XML ID of the attribute value.

Characters other than letters, digits and underscores are replaced by `_`.

No XML ID is generated when the template or the attribute value has no XML ID
(the result would not be predictable), or when the name is already used by
another record; the latter is logged as a warning.
