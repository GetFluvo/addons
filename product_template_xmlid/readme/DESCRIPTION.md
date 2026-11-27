This module gives every product created in the interface, or imported without
an XML ID, a predictable XML ID, so that it can be referenced in imports and
integrations without looking up its database id.

When a product is created, the module adds an XML ID
`product_template.<name>`, where `<name>` is made from:

- the internal reference of the product, for example `FURN-0001` becomes
  `product_template.furn_0001`;
- or, for products without an internal reference, its English name, for
  example *Desk Organizer (Large)* becomes
  `product_template.desk_organizer_large`.

The name is lowercased, accents are removed, and every other character than a
letter or a digit is replaced by `_`.

No XML ID is generated for products that already have one, such as products
imported with an *ID* column or loaded from data files, or when the name is
already used by another product; the latter is logged as a warning.

Together with `product_template_attribute_value_xmlid`, the attribute values of
these products get an XML ID too.
