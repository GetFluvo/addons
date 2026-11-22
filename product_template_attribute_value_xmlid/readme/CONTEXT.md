Product variants are built from `product.template.attribute.value` records:
one per attribute value on a product template (for example *Size: L* on a
*Desk Organizer*). Odoo gives these records no XML ID, so imports and
integrations have to look them up by database id, which differs between
databases.

With a predictable XML ID, extra prices, exclusions and variant combinations
can be imported and synchronized with external systems by reference.
