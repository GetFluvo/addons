# Copyright 2026 Strategic Efficiency B.V.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.model_create_multi
    def create(self, vals_list):
        """Generate the XML IDs of the templates created with the variants.

        The generation waits until the variants, and so the internal reference
        of their template, exist.
        """
        records = super(
            ProductProduct, self.with_context(product_template_xmlid_skip=True)
        ).create(vals_list)
        records = records.with_env(self.env)
        if not self.env.context.get("product_template_xmlid_skip"):
            records.product_tmpl_id._generate_xmlids()
        return records
