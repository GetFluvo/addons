import logging

from odoo.tests import TransactionCase, tagged

_logger = logging.getLogger(__name__)


@tagged("post_install", "-at_install")
class TestProductTemplateXmlid(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product_template = cls.env["product.template"].create(
            {
                "name": "Test Product Template",
            }
        )

    def test_to_xmlid(self):
        """Test the _to_xmlid method."""
        self.assertEqual(
            self.product_template._to_xmlid("Test.Product, Name"),
            "Test_Product__Name",
            "Should replace special characters",
        )
        self.assertEqual(
            self.product_template._to_xmlid("  Test Product  "),
            "__Test_Product__",
            "Should replace spaces",
        )
        self.assertEqual(
            self.product_template._to_xmlid("Test|Product\nName"),
            "Test_Product_Name",
            "Should replace more special characters",
        )
        self.assertEqual(
            self.product_template._to_xmlid("Test Product"),
            "Test_Product",
            "Should replace single space",
        )

    def test_generate_xmlid(self):
        """Test the _generate_xmlid method."""
        xml_id = self.product_template._generate_xmlid()
        self.assertEqual(
            xml_id, "product_Test_Product_Template", "Should generate correct XML ID"
        )

    def test_create_xmlid_if_not_exists(self):
        """Test the _create_xmlid_if_not_exists method."""
        # 1. Ensure no XML ID exists initially
        existing_xml_id = self.env["ir.model.data"].search(
            [
                ("model", "=", "product.template"),
                ("res_id", "=", self.product_template.id),
            ],
            limit=1,
        )
        self.assertFalse(existing_xml_id, "Should not have initial XML ID")

        # 2. Call the method to generate and create
        self.product_template._create_xmlid_if_not_exists()

        # 3. Verify XML ID is created
        created_xml_id = self.env["ir.model.data"].search(
            [
                ("model", "=", "product.template"),
                ("res_id", "=", self.product_template.id),
            ],
            limit=1,
        )
        self.assertTrue(created_xml_id, "Should have created XML ID")
        self.assertEqual(
            created_xml_id.name,
            "product_Test_Product_Template",
            "Should create correct XML ID name",
        )

        # 4. Call the method again - should NOT create a duplicate
        initial_count = self.env["ir.model.data"].search_count(
            [
                ("model", "=", "product.template"),
                ("res_id", "=", self.product_template.id),
            ]
        )
        self.product_template._create_xmlid_if_not_exists()
        final_count = self.env["ir.model.data"].search_count(
            [
                ("model", "=", "product.template"),
                ("res_id", "=", self.product_template.id),
            ]
        )
        self.assertEqual(
            initial_count, final_count, "Should not create duplicate XML ID"
        )

    def test_generate_missing_product_template_xmlids(self):
        """Test the generate_missing_product_template_xmlids method."""
        # 1. Create another product template without an XML ID
        another_template = self.env["product.template"].create(
            {"name": "Another Template"}
        )

        # 2. Call the method to generate missing XML IDs
        action = self.env["product.template"].generate_missing_product_template_xmlids()

        # 3. Verify the action type
        self.assertEqual(
            action["type"], "ir.actions.client", "Should return a client action"
        )
        self.assertEqual(
            action["tag"],
            "display_notification",
            "Should be a display_notification action",
        )

        # 4. Verify XML IDs are created
        created_xml_id_1 = self.env["ir.model.data"].search(
            [
                ("model", "=", "product.template"),
                ("res_id", "=", self.product_template.id),
            ],
            limit=1,
        )
        created_xml_id_2 = self.env["ir.model.data"].search(
            [
                ("model", "=", "product.template"),
                ("res_id", "=", another_template.id),
            ],
            limit=1,
        )
        self.assertTrue(
            created_xml_id_1, "Should have created XML ID for first template"
        )
        self.assertTrue(
            created_xml_id_2, "Should have created XML ID for second template"
        )
