import logging

from odoo import _, api, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def _to_xmlid(self, name):
        return (
            name.replace(".", "_")
            .replace(",", "_")
            .replace("\n", "_")
            .replace("|", "_")
            .replace(" ", "_")
            .strip()
        )

    def _generate_xmlid(self):
        """Helper function to generate an XML ID for this product template."""
        if not self.id:
            return None  # Cannot generate an XML ID for unsaved records

        # there should be a lower
        xml_id = "product_" + self._to_xmlid(self.name)

        return xml_id

    def _create_xmlid_if_not_exists(self):
        """
        Creates an ir.model.data record for this product template
        if one doesn't exist.
        """
        self.ensure_one()
        if not self.env["ir.model.data"].search(
            [("model", "=", self._name), ("res_id", "=", self.id)], limit=1
        ):
            try:
                xml_id = self._generate_xmlid()
                if xml_id:  # Only create if a valid XML ID was generated
                    self.env["ir.model.data"].create(
                        {
                            "module": "PRODUCT_TEMPLATE",
                            "name": xml_id,
                            "model": self._name,
                            "res_id": self.id,
                            "noupdate": True,
                        }
                    )

                    _logger.info(
                        f"Generated XML ID '{xml_id}' for product.template ID {self.id}"
                    )
            except Exception as e:
                _logger.error(
                    f"Error creating XML ID for product.template ID {self.id}: {e}"
                )
                self.env.rollback()  # Rollback in case of any database errors
                raise UserError(
                    _("Error generating XML ID for product template.")
                ) from e

    @api.model
    def generate_missing_product_template_xmlids(self):
        """Generate XML IDs for product templates that are missing them."""

        templates_without_xmlid = self.search(
            [
                (
                    "id",
                    "not in",
                    self.env["ir.model.data"]
                    .search([("model", "=", "product.template")])
                    .mapped("res_id"),
                )
            ]
        )

        for template in templates_without_xmlid:
            template._create_xmlid_if_not_exists()

        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": _("XML IDs Generated"),
                "message": _("XML IDs for product templates have been generated."),
                "type": "success",
            },
        }
