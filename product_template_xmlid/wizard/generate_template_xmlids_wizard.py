from odoo import models


class GenerateTemplateXmlidsWizard(models.TransientModel):
    _name = "generate.template.xmlids.wizard"
    _description = "Generate Product Template XML IDs"

    def generate_xmlids(self):
        return self.env["product.template"].generate_missing_product_template_xmlids()
