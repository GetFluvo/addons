# Copyright 2025 Strategic Efficiency B.V.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from lxml import etree

from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestProductTemplateAttributeLineMenu(TransactionCase):
    def test_menu_opens_lines(self):
        menu = self.env.ref(
            "product_template_attribute_line.menu_product_template_attribute_line"
        )
        self.assertEqual(menu.action.res_model, "product.template.attribute.line")

    def test_list_view_allows_create(self):
        arch = self.env["product.template.attribute.line"].get_view(view_type="list")[
            "arch"
        ]
        self.assertEqual(etree.fromstring(arch).get("create"), "1")
