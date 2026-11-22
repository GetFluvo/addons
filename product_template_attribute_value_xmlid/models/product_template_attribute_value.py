# Copyright 2025 Strategic Efficiency B.V.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

import logging
import re

from odoo import _, api, models

_logger = logging.getLogger(__name__)

# Namespace of the generated XML IDs. Deliberately not the name of this
# module: on uninstall Odoo deletes every record referenced by an XML ID of
# the module, which would delete the product.template.attribute.value records.
XMLID_MODULE = "product_template_attribute_value"


class ProductTemplateAttributeValue(models.Model):
    _inherit = "product.template.attribute.value"

    @api.model_create_multi
    def create(self, vals_list):
        """Generate the XML IDs of the new records."""
        records = super().create(vals_list)
        records._generate_xmlids()
        return records

    def _get_generated_xmlid_name(self):
        """Return the XML ID name for this record, or ``""`` if none can be made.

        The name is ``<template XML ID name>_<attribute value XML ID name>``.
        Without an XML ID on the template or on the attribute value the name
        would not be predictable, so none is returned.
        """
        self.ensure_one()
        template_name = self._get_xmlid_name(self.product_tmpl_id)
        value_name = self._get_xmlid_name(self.product_attribute_value_id)
        if not template_name or not value_name:
            return ""
        return re.sub(r"\W", "_", f"{template_name}_{value_name}")

    def _generate_xmlids(self):
        """Create the XML IDs of the records in ``self`` that can get one.

        A record is skipped when no predictable name can be made for it, or
        when that name is already taken by another record.
        """
        IrModelData = self.env["ir.model.data"].sudo()
        names = {}
        for record in self:
            name = record._get_generated_xmlid_name()
            if name:
                names[record] = name
        if not names:
            return self.browse()
        taken = {
            data.name: data.res_id
            for data in IrModelData.search(
                [
                    ("module", "=", XMLID_MODULE),
                    ("name", "in", list(names.values())),
                ]
            )
        }
        vals_list = []
        created = self.browse()
        for record, name in names.items():
            if name in taken:
                if taken[name] != record.id:
                    _logger.warning(
                        "XML ID %s.%s already points to %s(%s), not set on %s",
                        XMLID_MODULE,
                        name,
                        self._name,
                        taken[name],
                        record,
                    )
                continue
            taken[name] = record.id
            created |= record
            vals_list.append(
                {
                    "module": XMLID_MODULE,
                    "name": name,
                    "model": self._name,
                    "res_id": record.id,
                    "noupdate": True,
                }
            )
        IrModelData.create(vals_list)
        return created

    @api.model
    def generate_attribute_value_xmlids(self, *args):
        """Generate the missing XML IDs of all product.template.attribute.value.

        ``*args`` takes the record ids that a button of type ``object`` passes.
        """
        with_xmlid = (
            self.env["ir.model.data"]
            .sudo()
            .search([("module", "=", XMLID_MODULE), ("model", "=", self._name)])
            .mapped("res_id")
        )
        created = self.search([("id", "not in", with_xmlid)])._generate_xmlids()
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": _("XML IDs Created"),
                "message": _(
                    "%(count)s XML IDs for product template attribute values "
                    "have been generated.",
                    count=len(created),
                ),
                "type": "success",
            },
        }

    @api.model
    def _get_xmlid_name(self, record):
        """Return the name, without module, of the first XML ID of ``record``."""
        if not record:
            return ""
        data = (
            self.env["ir.model.data"]
            .sudo()
            .search(
                [("model", "=", record._name), ("res_id", "=", record.id)],
                order="id",
                limit=1,
            )
        )
        return data.name or ""
