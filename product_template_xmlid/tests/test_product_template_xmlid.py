# Copyright 2026 Strategic Efficiency B.V.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo.tests.common import TransactionCase, tagged

from ..models.product_template import XMLID_MODULE

TEMPLATE = "product.template"


@tagged("post_install", "-at_install")
class TestProductTemplateXMLID(TransactionCase):
    def _generated(self, templates):
        return self.env["ir.model.data"].search(
            [
                ("module", "=", XMLID_MODULE),
                ("model", "=", TEMPLATE),
                ("res_id", "in", templates.ids),
            ]
        )

    def test_xmlid_from_internal_reference(self):
        template = self.env[TEMPLATE].create(
            {"name": "Desk Organizer", "default_code": "FURN-0001"}
        )
        self.assertEqual(self.env.ref(f"{XMLID_MODULE}.furn_0001"), template)
        self.assertTrue(self._generated(template).noupdate)

    def test_xmlid_from_name(self):
        templates = self.env[TEMPLATE].create(
            [{"name": "Desk Organizer (Large)"}, {"name": "  Café Crème  "}]
        )
        self.assertEqual(
            set(self._generated(templates).mapped("name")),
            {"desk_organizer_large", "cafe_creme"},
        )

    def test_xmlid_from_variant(self):
        variant = self.env["product.product"].create(
            {"name": "Variant Lamp", "default_code": "LAMP-1"}
        )
        self.assertEqual(
            self.env.ref(f"{XMLID_MODULE}.lamp_1"), variant.product_tmpl_id
        )

    def test_no_xmlid_without_name(self):
        template = self.env[TEMPLATE].create({"name": "???"})
        self.assertFalse(self._generated(template))

    def test_taken_name_is_skipped(self):
        """A name taken by another record is logged, not overwritten."""
        first = self.env[TEMPLATE].create({"name": "Chair"})
        with self.assertLogs(
            "odoo.addons.product_template_xmlid.models.product_template",
            level="WARNING",
        ) as logs:
            second = self.env[TEMPLATE].create({"name": "Chair"})
        self.assertIn(f"{XMLID_MODULE}.chair", logs.output[0])
        self.assertFalse(self._generated(second))
        self.assertEqual(self.env.ref(f"{XMLID_MODULE}.chair"), first)

    def test_import_with_xmlid(self):
        """An imported XML ID is the only XML ID of the record."""
        result = self.env[TEMPLATE].load(
            ["id", "name"], [["imported_chair", "Imported Chair"]]
        )
        template = self.env[TEMPLATE].browse(result["ids"])
        self.assertEqual(self.env.ref("__import__.imported_chair"), template)
        self.assertFalse(self._generated(template))

    def test_import_without_xmlid(self):
        result = self.env[TEMPLATE].load(["name"], [["Imported Table"]])
        template = self.env[TEMPLATE].browse(result["ids"])
        self.assertEqual(self.env.ref(f"{XMLID_MODULE}.imported_table"), template)

    def test_action_generate_xmlids(self):
        templates = self.env[TEMPLATE].create(
            [{"name": "Backfill One"}, {"name": "Backfill Two"}]
        )
        self._generated(templates).unlink()
        action = templates.action_generate_xmlids()
        self.assertEqual(action["tag"], "display_notification")
        self.assertIn("2", action["params"]["message"])
        self.assertEqual(len(self._generated(templates)), 2)

        # Nothing left to do on a second run.
        action = templates.action_generate_xmlids()
        self.assertIn("0", action["params"]["message"])
        self.assertEqual(len(self._generated(templates)), 2)

    def test_attribute_values_get_xmlid(self):
        """With product_template_attribute_value_xmlid, the values follow."""
        ptav_model = self.env["product.template.attribute.value"]
        if not hasattr(ptav_model, "_generate_xmlids"):
            self.skipTest("product_template_attribute_value_xmlid not installed")
        attribute = self.env["product.attribute"].create(
            {"name": "Test Size", "create_variant": "always"}
        )
        value = self.env["product.attribute.value"].create(
            {"name": "L", "attribute_id": attribute.id}
        )
        self.env["ir.model.data"].create(
            {
                "module": "test_product_template_xmlid",
                "name": "size_l",
                "model": value._name,
                "res_id": value.id,
            }
        )
        template = self.env[TEMPLATE].create(
            {
                "name": "Sized Desk",
                "attribute_line_ids": [
                    (
                        0,
                        0,
                        {
                            "attribute_id": attribute.id,
                            "value_ids": [(6, 0, value.ids)],
                        },
                    )
                ],
            }
        )
        self.assertEqual(
            self.env.ref("product_template_attribute_value.sized_desk_size_l"),
            template.attribute_line_ids.product_template_value_ids,
        )
