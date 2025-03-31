from odoo.tests.common import TransactionCase, tagged
from odoo import fields, Command

@tagged("post_install", "-at_install")
class TestProductTemplateAttributeValueXMLID(TransactionCase):

    def setUp(self):
        super().setUp()
        # Create common product template and attribute (dynamic variant creation)
        self.product_template = self.env['product.template'].create({
            'name': 'Test Template',
        })
        self.attribute = self.env['product.attribute'].create({
            'name': 'Test Attribute',
            'create_variant': 'dynamic',
        })
        self.attribute_value = self.env['product.attribute.value'].create({
            'name': 'Test Value',
            'attribute_id': self.attribute.id,
        })

    def test_xmlid_generation_on_ptav_creation(self):
        """
        Test that an XML ID is automatically generated for the
        product.template.attribute.value record when it is created
        automatically during variant creation.
        """
        # 1. Create a product.template.attribute.line
        attribute_line = self.env['product.template.attribute.line'].create({
            'product_tmpl_id': self.product_template.id,
            'attribute_id': self.attribute.id,
            'value_ids': [(6, 0, [self.attribute_value.id])],
        })

        # 2. Trigger Variant Creation (Simulate Selection)
        #    This forces Odoo to create the product.template.attribute.value record
        context = {'default_product_tmpl_id': self.product_template.id}
        self.product_template.with_context(context).write({
            'attribute_line_ids': [(1, attribute_line.id, {'value_ids': [(6, 0, [self.attribute_value.id])]})]
        })

        # 3. Find the Automatically Created product.template.attribute.value
        ptav = self.env['product.template.attribute.value'].search([
            ('attribute_line_id', '=', attribute_line.id),
            ('product_attribute_value_id', '=', self.attribute_value.id)
        ], limit=1)
        self.assertTrue(ptav, "product.template.attribute.value was not created")

        # 4. Check for XML ID on the product.template.attribute.value
        xml_id = self.env['ir.model.data'].search([
            ('model', '=', 'product.template.attribute.value'),
            ('res_id', '=', ptav.id),
        ], limit=1)
        self.assertTrue(xml_id, f"No XML ID generated for product.template.attribute.value: {ptav.id}")

    def _get_xml_id(self, record):
        """Helper function to get the XML ID of a record."""
        if not record:
            return ''
        xml_ids = self.env['ir.model.data'].search([
            ('model', '=', record._name),
            ('res_id', '=', record.id),
        ], limit=1)
        return xml_ids.name if xml_ids else ''
