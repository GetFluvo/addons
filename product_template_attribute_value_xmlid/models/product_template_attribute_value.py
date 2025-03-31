from odoo import _, api, models


class ProductTemplateAttributeValueXMLID(models.Model):
    _inherit = "product.template.attribute.value"

    @api.model_create_multi
    def create(self, vals_list):
        """
        Overrides the create method to automatically generate XML IDs.
        """
        records = super().create(vals_list)
        for record in records:
            self._generate_xmlid_for_record(
                record
            )  # Generate XML ID for each new record
        return records

    def _generate_xmlid_for_record(self, attribute_value):
        """
        Generates the XML ID for a given product.template.attribute.value record.
        """
        # 2. Generate the XML ID using XML IDs of related records
        prod_templ_id = (
            self._get_xml_id(attribute_value.product_tmpl_id)
            if attribute_value.product_tmpl_id
            else ""
        )
        (
            self._get_xml_id(attribute_value.attribute_id)
            if attribute_value.attribute_id
            else ""
        )
        attribute_value_id = (
            self._get_xml_id(attribute_value.product_attribute_value_id)
            if attribute_value.product_attribute_value_id
            else ""
        )

        xml_id = f"{prod_templ_id}_{attribute_value_id}".replace(" ", "_")

        # 3. Create the ir.model.data record
        try:
            self.env["ir.model.data"].create(
                {
                    "module": "product_template_attribute_value",
                    "name": xml_id,
                    "model": "product.template.attribute.value",
                    "res_id": attribute_value.id,
                    "noupdate": True,
                }
            )
        except Exception as e:
            # self.env.cr.rollback()  # Removed direct cr.rollback()
            # self.env.cr.commit()    # Removed direct cr.commit()
            self.env.logger.error(
                f"Error creating XML ID for product.template.attribute.value: {e}"
            )
            raise  # Re-raise the exception to allow Odoo to handle it

    @api.model
    def generate_attribute_value_xmlids(self, *args):
        """
        Generates XML IDs for product.template.attribute.value records
        using the format: XMLID = prod_templ_id + attribute_id + attribute_value_id
        """
        # 1. Get the product.template.attribute.value records that DO NOT have an XML ID
        attribute_values_without_xmlid = self.env[
            "product.template.attribute.value"
        ].search(
            [
                (
                    "id",
                    "not in",
                    self.env["ir.model.data"]
                    .search([("model", "=", "product.template.attribute.value")])
                    .mapped("res_id"),
                )
            ]
        )

        for attribute_value in attribute_values_without_xmlid:
            self._generate_xmlid_for_record(attribute_value)

        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": _("XML IDs Created"),
                "message": _(
                    "XML IDs for product.template.attribute.value",
                    "records have been generated.",
                ),
                "type": "success",
            },
        }

    def _get_xml_id(self, record):
        """Helper function to get the XML ID of a record."""
        if not record:
            return ""
        xml_ids = self.env["ir.model.data"].search(
            [
                ("model", "=", record._name),
                ("res_id", "=", record.id),
            ],
            limit=1,
        )
        return xml_ids.name if xml_ids else ""
