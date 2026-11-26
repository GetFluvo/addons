# Copyright 2026 Strategic Efficiency B.V.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

import base64

from odoo.exceptions import AccessError, ValidationError
from odoo.tests.common import TransactionCase, new_test_user, tagged


@tagged("post_install", "-at_install")
class TestImportResId(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner, cls.partner2, cls.partner_no_xmlid = cls.env["res.partner"].create(
            [{"name": "Old Customer"}, {"name": "Other"}, {"name": "None"}]
        )
        for record, name in [(cls.partner, "customer"), (cls.partner2, "other")]:
            cls.env["ir.model.data"].create(
                {
                    "module": "legacy",
                    "name": name,
                    "model": record._name,
                    "res_id": record.id,
                }
            )
        cls.user = new_test_user(cls.env, login="clerk", groups="base.group_user")

    def _attachment_vals(self, **vals):
        return {"name": "a.txt", "raw": b"hello", **vals}

    def test_attachment_create(self):
        attachment = self.env["ir.attachment"].create(
            self._attachment_vals(res_external_id="legacy.customer")
        )
        self.assertEqual(attachment.res_model, "res.partner")
        self.assertEqual(attachment.res_id, self.partner.id)
        self.assertEqual(attachment.res_external_id, "legacy.customer")

    def test_message_create_multi(self):
        messages = self.env["mail.message"].create(
            [
                {"body": "One", "res_external_id": "legacy.customer"},
                {"body": "Two", "res_external_id": " legacy.other "},
                {"body": "Three", "res_external_id": False},
            ]
        )
        self.assertEqual(
            [(m.model, m.res_id) for m in messages],
            [
                ("res.partner", self.partner.id),
                ("res.partner", self.partner2.id),
                (False, 0),
            ],
        )
        self.assertEqual(
            messages.mapped("res_external_id"),
            ["legacy.customer", "legacy.other", False],
        )
        self.assertIn(messages[0], self.partner.message_ids)

    def test_message_write(self):
        message = self.env["mail.message"].create({"body": "Moved"})
        message.write({"res_external_id": "legacy.other"})
        self.assertEqual(
            (message.model, message.res_id), ("res.partner", self.partner2.id)
        )
        message.res_external_id = "legacy.customer"
        self.assertEqual(message.res_id, self.partner.id)

    def test_message_write_non_admin(self):
        """Odoo only allows administrators to move a message."""
        message = self.env["mail.message"].create(
            {"body": "Mine", "res_external_id": "legacy.customer"}
        )
        with self.assertRaises(AccessError):
            message.with_user(self.user).write({"res_external_id": "legacy.other"})

    def test_access_checked_on_document(self):
        """The access checks of the standard create apply to the document."""
        param = self.env["ir.config_parameter"].create({"key": "k", "value": "v"})
        self.env["ir.model.data"].create(
            {
                "module": "legacy",
                "name": "param",
                "model": param._name,
                "res_id": param.id,
            }
        )
        with self.assertRaises(AccessError):
            self.env["ir.attachment"].with_user(self.user).create(
                self._attachment_vals(res_external_id="legacy.param")
            )

    def test_unknown_xmlid(self):
        for xmlid in ("legacy.missing", "customer"):
            with self.subTest(xmlid=xmlid), self.assertRaises(ValidationError):
                self.env["mail.message"].create(
                    {"body": "Lost", "res_external_id": xmlid}
                )

    def test_document_without_xmlid(self):
        attachment = self.env["ir.attachment"].create(
            self._attachment_vals(
                res_model="res.partner", res_id=self.partner_no_xmlid.id
            )
        )
        self.assertFalse(attachment.res_external_id)

    def test_load_chatter(self):
        """Import attachments, then messages with them, on a partner."""
        result = self.env["ir.attachment"].load(
            ["id", "name", "raw", "res_external_id"],
            [
                [
                    "legacy.attachment_1",
                    "a.txt",
                    base64.b64encode(b"hello").decode(),
                    "legacy.customer",
                ]
            ],
        )
        self.assertFalse(result["messages"], result["messages"])
        attachment = self.env.ref("legacy.attachment_1")
        self.assertEqual(attachment.raw.content, b"hello")
        result = self.env["mail.message"].load(
            ["body", "message_type", "res_external_id", "attachment_ids/id"],
            [["<p>Old note</p>", "comment", "legacy.customer", "legacy.attachment_1"]],
        )
        self.assertFalse(result["messages"], result["messages"])
        message = self.env["mail.message"].browse(result["ids"])
        self.assertIn(message, self.partner.message_ids)
        self.assertEqual(message.attachment_ids, attachment)
        self.assertEqual(
            (attachment.res_model, attachment.res_id), ("res.partner", self.partner.id)
        )

    def test_load_activity(self):
        """Import a to-do with deadline and assignee on a partner."""
        result = self.env["mail.activity"].load(
            [
                "activity_type_id/id",
                "summary",
                "date_deadline",
                "user_id/id",
                "res_external_id",
            ],
            [
                [
                    "mail.mail_activity_data_todo",
                    "Call back",
                    "2026-12-01",
                    "base.user_admin",
                    "legacy.customer",
                ]
            ],
        )
        self.assertFalse(result["messages"], result["messages"])
        activity = self.env["mail.activity"].browse(result["ids"])
        self.assertEqual(
            (activity.res_model, activity.res_id, activity.res_name),
            ("res.partner", self.partner.id, "Old Customer"),
        )
        self.assertEqual(activity.res_external_id, "legacy.customer")
        self.assertIn(activity, self.partner.activity_ids)

    def test_activity_write(self):
        activity = self.env["mail.activity"].create(
            {
                "activity_type_id": self.env.ref("mail.mail_activity_data_todo").id,
                "res_external_id": "legacy.customer",
            }
        )
        activity.write({"res_external_id": "legacy.other"})
        self.assertEqual(
            (activity.res_model, activity.res_id), ("res.partner", self.partner2.id)
        )

    def test_activity_unknown_xmlid(self):
        with self.assertRaises(ValidationError):
            self.env["mail.activity"].create(
                {
                    "activity_type_id": self.env.ref("mail.mail_activity_data_todo").id,
                    "res_external_id": "legacy.missing",
                }
            )
