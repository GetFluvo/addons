import logging

from odoo import _, api, models

_logger = logging.getLogger(__name__)


class ProductTemplateAttributeValueXMLID(models.Model):
    _inherit = "product.template.attribute.value"

    @api.model_create_multi
    def create(self, vals_list):
        """
        Overrides the create method to automatically generate XML IDs.
        """
        records = super().create(vals_list)
        xml_ids_to_create = []  # List to store XML IDs to create

        for record in records:
            xml_id = self._generate_xmlid_for_record_name(record)
            if xml_id:  # Only proceed if xml_id is not empty
                xml_ids_to_create.append((record, xml_id))

        existing_xml_ids = self.env["ir.model.data"].search(
            [
                ("model", "=", "product.template.attribute.value"),
                ("name", "in", [xml_id for _, xml_id in xml_ids_to_create]),
            ]
        )
        existing_xml_id_names = set(existing_xml_ids.mapped("name"))

        for record, xml_id in xml_ids_to_create:
            if xml_id not in existing_xml_id_names:
                try:
                    self.env["ir.model.data"].create(
                        {
                            "module": "product_template_attribute_value",
                            "name": xml_id,
                            "model": "product.template.attribute.value",
                            "res_id": record.id,
                            "noupdate": True,
                        }
                    )
                except Exception as e:
                    _logger.error(f"Error creating XML ID: {e}")
                    raise  # Re-raise the exception

        return records

    @api.model
    def _generate_xmlid_for_record_name(self, attribute_value):
        """
        Generates the XML ID name (not the record) for a given
        product.template.attribute.value record.
        """
        prod_templ_id = (
            self._get_xml_id(attribute_value.product_tmpl_id)
            if attribute_value.product_tmpl_id
            else None
        )
        attribute_id = (  # noqa
            self._get_xml_id(attribute_value.attribute_id)
            if attribute_value.attribute_id
            else ""
        )
        attribute_value_id = (
            self._get_xml_id(attribute_value.product_attribute_value_id)
            if attribute_value.product_attribute_value_id
            else ""
        )

        if not prod_templ_id:
            return None  # Return None if any part is missing

        return f"{prod_templ_id}_{attribute_value_id}".replace(" ", "_")

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
            self._generate_xmlid_for_record_name(attribute_value)

        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": _("XML IDs Created"),
                "message": _(
                    "XML IDs for product.template.attribute.value records have been generated."  # noqa
                ),
                "type": "success",
            },
        }

    @api.model
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
