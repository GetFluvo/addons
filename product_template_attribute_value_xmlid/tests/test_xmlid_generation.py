# Copyright 2025 Strategic Efficiency B.V.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo.tests.common import TransactionCase, tagged

from ..models.product_template_attribute_value import XMLID_MODULE

PTAV = "product.template.attribute.value"


@tagged("post_install", "-at_install")
class TestProductTemplateAttributeValueXMLID(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.attribute = cls.env["product.attribute"].create(
            {"name": "Test Attribute", "create_variant": "always"}
        )
        cls.value_red, cls.value_blue = cls.env["product.attribute.value"].create(
            [
                {"name": "Red", "attribute_id": cls.attribute.id},
                {"name": "Blue", "attribute_id": cls.attribute.id},
            ]
        )
        cls._set_xmlid(cls.value_red, "value_red")
        cls._set_xmlid(cls.value_blue, "value_blue")
        cls.template = cls.env["product.template"].create({"name": "Test Template"})
        cls._set_xmlid(cls.template, "tmpl")

    @classmethod
    def _set_xmlid(cls, record, name, module="test_ptav_xmlid"):
        cls.env["ir.model.data"].create(
            {
                "module": module,
                "name": name,
                "model": record._name,
                "res_id": record.id,
            }
        )

    def _add_values(self, template, values):
        template.write(
            {
                "attribute_line_ids": [
                    (
                        0,
                        0,
                        {
                            "attribute_id": self.attribute.id,
                            "value_ids": [(6, 0, values.ids)],
                        },
                    )
                ]
            }
        )
        return template.attribute_line_ids.product_template_value_ids

    def _generated(self, ptavs):
        return self.env["ir.model.data"].search(
            [
                ("module", "=", XMLID_MODULE),
                ("model", "=", PTAV),
                ("res_id", "in", ptavs.ids),
            ]
        )

    def test_xmlid_on_create(self):
        ptavs = self._add_values(self.template, self.value_red | self.value_blue)
        self.assertEqual(len(ptavs), 2)
        red = ptavs.filtered(lambda v: v.product_attribute_value_id == self.value_red)
        self.assertEqual(
            self.env.ref(f"{XMLID_MODULE}.tmpl_value_red"),
            red,
        )
        self.assertEqual(
            set(self._generated(ptavs).mapped("name")),
            {"tmpl_value_red", "tmpl_value_blue"},
        )
        self.assertTrue(all(self._generated(ptavs).mapped("noupdate")))

    def test_no_xmlid_without_template_xmlid(self):
        """Templates without an XML ID get none, and do not collide."""
        templates = self.env["product.template"].create(
            [{"name": "No XML ID 1"}, {"name": "No XML ID 2"}]
        )
        ptavs = self._add_values(templates[0], self.value_red)
        ptavs |= self._add_values(templates[1], self.value_red)
        self.assertEqual(len(ptavs), 2)
        self.assertFalse(self._generated(ptavs))

    def test_no_xmlid_without_value_xmlid(self):
        value = self.env["product.attribute.value"].create(
            {"name": "Green", "attribute_id": self.attribute.id}
        )
        ptavs = self._add_values(self.template, value)
        self.assertFalse(self._generated(ptavs))

    def test_name_is_sanitized(self):
        template = self.env["product.template"].create({"name": "Dashed"})
        self._set_xmlid(template, "tmpl-dash")
        ptavs = self._add_values(template, self.value_red)
        self.assertEqual(
            self._generated(ptavs).name,
            "tmpl_dash_value_red",
        )

    def test_taken_name_is_skipped(self):
        """A name taken by another record is logged, not overwritten."""
        template = self.env["product.template"].create({"name": "Taken"})
        self._set_xmlid(template, "taken")
        other_ptav = self._add_values(self.template, self.value_blue)
        self._set_xmlid(other_ptav, "taken_value_red", module=XMLID_MODULE)
        with self.assertLogs(
            "odoo.addons.product_template_attribute_value_xmlid.models."
            "product_template_attribute_value",
            level="WARNING",
        ) as logs:
            ptavs = self._add_values(template, self.value_red)
        self.assertIn("taken_value_red", logs.output[0])
        self.assertFalse(self._generated(ptavs))
        self.assertEqual(self.env.ref(f"{XMLID_MODULE}.taken_value_red"), other_ptav)

    def test_generate_missing_xmlids(self):
        ptavs = self._add_values(self.template, self.value_red | self.value_blue)
        # Catch up on records created before the module was installed (demo).
        self.env[PTAV].generate_attribute_value_xmlids()
        self._generated(ptavs).unlink()
        self.assertFalse(self._generated(ptavs))

        # Called from the form's button, which passes the record ids.
        action = self.env[PTAV].generate_attribute_value_xmlids(ptavs[:1].ids)
        self.assertEqual(action["tag"], "display_notification")
        self.assertIn("2", action["params"]["message"])
        self.assertEqual(len(self._generated(ptavs)), 2)

        # Nothing left to do on a second run.
        action = self.env[PTAV].generate_attribute_value_xmlids()
        self.assertIn("0", action["params"]["message"])
        self.assertEqual(len(self._generated(ptavs)), 2)

    def test_generate_xmlids_empty(self):
        self.assertFalse(self.env[PTAV]._generate_xmlids())
        self.assertEqual(self.env[PTAV]._get_xmlid_name(self.env[PTAV]), "")

    def test_generate_is_idempotent(self):
        ptavs = self._add_values(self.template, self.value_red)
        with self.assertNoLogs(level="WARNING"):
            self.assertEqual(ptavs._generate_xmlids(), ptavs.browse())
        self.assertEqual(len(self._generated(ptavs)), 1)
