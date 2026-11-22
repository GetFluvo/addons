# Copyright 2026 Strategic Efficiency B.V.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ImportResIdMixin(models.AbstractModel):
    """Set the document of a record by the XML ID of that document.

    For models that link to any document with a model name field and a
    ``res_id`` field, like ``mail.message`` and ``ir.attachment``.
    """

    _name = "import.res.id.mixin"
    _description = "Document by XML ID"

    # Name of the field holding the model name of the document.
    _res_model_field = "res_model"

    res_external_id = fields.Char(
        string="Document XML ID",
        compute="_compute_res_external_id",
        readonly=False,
        help="XML ID of the document, as module.name. Setting it sets the "
        "model and the id of the document.",
    )

    def _compute_res_external_id(self):
        IrModelData = self.env["ir.model.data"].sudo()
        for record in self:
            model, res_id = record[self._res_model_field], record.res_id
            data = (
                IrModelData.search(
                    [("model", "=", model), ("res_id", "=", res_id)],
                    order="id",
                    limit=1,
                )
                if model and res_id
                else IrModelData
            )
            record.res_external_id = f"{data.module}.{data.name}" if data else False

    @api.model
    def _import_res_id_resolve(self, vals):
        """Replace ``res_external_id`` in ``vals`` by the model and res_id."""
        xmlid = vals.pop("res_external_id", None)
        if not xmlid:
            return vals
        xmlid = xmlid.strip()
        model, res_id = self.env["ir.model.data"]._xmlid_to_res_model_res_id(xmlid)
        if not model:
            raise ValidationError(
                self.env._(
                    "Document XML ID %(xmlid)s does not exist. It must be the "
                    "complete XML ID, as module.name.",
                    xmlid=xmlid,
                )
            )
        vals[self._res_model_field] = model
        vals["res_id"] = res_id
        return vals
