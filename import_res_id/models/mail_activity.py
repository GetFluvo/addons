# Copyright 2026 Strategic Efficiency B.V.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, models


class MailActivity(models.Model):
    _name = "mail.activity"
    _inherit = ["mail.activity", "import.res.id.mixin"]

    # Resolved before the standard create and write, so that their access
    # checks apply to the document.
    @api.model_create_multi
    def create(self, vals_list):
        vals_list = [self._import_res_id_resolve(dict(vals)) for vals in vals_list]
        return super().create(vals_list)

    def write(self, vals):
        return super().write(self._import_res_id_resolve(dict(vals)))

    @api.model
    def _import_res_id_set_model(self, vals, model):
        """``res_model`` is a readonly related of ``res_model_id``."""
        vals["res_model_id"] = self.env["ir.model"]._get_id(model)
