# Copyright 2026 Strategic Efficiency B.V.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, models


class IrAttachment(models.Model):
    _name = "ir.attachment"
    _inherit = ["ir.attachment", "import.res.id.mixin"]

    # Resolved before the standard create and write, so that their access
    # checks apply to the document.
    @api.model_create_multi
    def create(self, vals_list):
        vals_list = [self._import_res_id_resolve(dict(vals)) for vals in vals_list]
        return super().create(vals_list)

    def write(self, vals):
        return super().write(self._import_res_id_resolve(dict(vals)))
