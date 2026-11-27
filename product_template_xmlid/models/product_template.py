# Copyright 2026 Strategic Efficiency B.V.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

import logging
import re
import unicodedata

from odoo import api, models

_logger = logging.getLogger(__name__)

# Namespace of the generated XML IDs. Deliberately not the name of this
# module: on uninstall Odoo deletes every record referenced by an XML ID of
# the module, which would delete the products.
XMLID_MODULE = "product_template"


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model_create_multi
    def create(self, vals_list):
        """Generate the XML IDs of the new records.

        The generation waits until the internal reference, which Odoo writes
        after the creation of the variants, is set.
        """
        records = super(
            ProductTemplate, self.with_context(product_template_xmlid_skip=True)
        ).create(vals_list)
        records = records.with_env(self.env)
        if not self.env.context.get("product_template_xmlid_skip"):
            records._generate_xmlids()
        return records

    def _load_records(self, *args, **kwargs):
        """Leave records that are imported or loaded with an XML ID alone.

        ``load()`` and data files create the records before they add their
        XML ID, so the generation is postponed until that XML ID exists.
        """
        records = super(
            ProductTemplate, self.with_context(product_template_xmlid_skip=True)
        )._load_records(*args, **kwargs)
        records = records.with_env(self.env)
        if not self.env.context.get("product_template_xmlid_skip"):
            records._generate_xmlids()
        return records

    def _get_generated_xmlid_name(self):
        """Return the XML ID name for this record, or ``""`` if none can be made.

        The name is made from the internal reference, or from the English name
        of products without one: lowercase, accents removed, and every other
        character than a letter or digit replaced by an underscore.
        """
        self.ensure_one()
        key = self.default_code or self.with_context(lang="en_US").name or ""
        key = unicodedata.normalize("NFKD", key).encode("ascii", "ignore").decode()
        return re.sub(r"[^a-z0-9]+", "_", key.lower()).strip("_")

    def _generate_xmlids(self):
        """Create the XML IDs of the records in ``self`` that can get one.

        A record is skipped when it already has an XML ID, when no name can be
        made for it, or when that name is already taken by another record.
        """
        IrModelData = self.env["ir.model.data"].sudo()
        with_xmlid = set(
            IrModelData.search(
                [("model", "=", self._name), ("res_id", "in", self.ids)]
            ).mapped("res_id")
        )
        names = {}
        for record in self:
            if record.id in with_xmlid:
                continue
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
        created._generate_attribute_value_xmlids()
        return created

    def _generate_attribute_value_xmlids(self):
        """Name the attribute values of templates that just got an XML ID.

        The attribute values are created before the template gets its XML ID,
        so ``product_template_attribute_value_xmlid``, when installed, could
        not name them yet.
        """
        ptavs = self.attribute_line_ids.product_template_value_ids
        if hasattr(ptavs, "_generate_xmlids"):
            ptavs._generate_xmlids()

    def action_generate_xmlids(self):
        """Generate the missing XML IDs of the selected products."""
        created = self._generate_xmlids()
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": self.env._("XML IDs Created"),
                "message": self.env._(
                    "%(count)s of the %(total)s selected products got an XML ID.",
                    count=len(created),
                    total=len(self),
                ),
                "type": "success",
            },
        }
