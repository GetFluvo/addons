# Copyright 2026 Strategic Efficiency B.V.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import fields
from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase, new_test_user, tagged

# Odoo stores naive datetimes, in UTC.
OLD = fields.Datetime.to_datetime("2016-01-02 03:04:05")
OLDER = fields.Datetime.to_datetime("2015-06-07 08:09:10")


@tagged("post_install", "-at_install")
class TestImportMetadata(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = new_test_user(cls.env, login="author", name="Original Author")
        cls.editor = new_test_user(cls.env, login="editor", name="Original Editor")
        cls.clerk = new_test_user(
            cls.env, login="clerk", groups="base.group_user,base.group_partner_manager"
        )
        cls.Partner = cls.env["res.partner"].with_context(write_metadata=True)

    def _metadata(self, record):
        """Read the metadata from the database, not from the cache."""
        record.invalidate_recordset()
        return (
            record.create_uid,
            record.create_date,
            record.write_uid,
            record.write_date,
        )

    def test_create(self):
        partner = self.Partner.create(
            {
                "name": "Old",
                "create_uid": self.author.id,
                "create_date": OLD,
                "write_uid": self.editor.id,
                "write_date": "2016-01-02 03:04:05",
            }
        )
        # The cache is up to date in the same transaction.
        self.assertEqual(partner.create_uid, self.author)
        self.assertEqual(partner.create_date, OLD)
        self.assertEqual(self._metadata(partner), (self.author, OLD, self.editor, OLD))

    def test_create_partial(self):
        partner = self.Partner.create({"name": "Old", "create_date": OLD})
        create_uid, create_date, write_uid, write_date = self._metadata(partner)
        self.assertEqual(create_date, OLD)
        self.assertEqual(create_uid, self.env.user)
        self.assertEqual(write_uid, self.env.user)
        self.assertNotEqual(write_date, OLD)

    def test_create_multi(self):
        vals_list = [
            {"name": "A", "create_uid": self.author.id, "create_date": OLD},
            {"name": "B", "create_uid": self.editor, "create_date": OLDER},
            {"name": "C"},
            {"name": "D", "create_uid": self.author.id, "create_date": OLD},
        ]
        a, b, c, d = self.Partner.create(vals_list)
        self.assertEqual(self._metadata(a)[:2], (self.author, OLD))
        self.assertEqual(self._metadata(b)[:2], (self.editor, OLDER))
        self.assertEqual(self._metadata(c)[0], self.env.user)
        self.assertNotEqual(self._metadata(c)[1], OLD)
        self.assertEqual(self._metadata(d)[:2], (self.author, OLD))
        # The values of the caller are left untouched.
        self.assertEqual(vals_list[0]["create_uid"], self.author.id)

    def test_create_without_context(self):
        partner = self.env["res.partner"].create(
            {"name": "New", "create_uid": self.author.id, "create_date": OLD}
        )
        self.assertEqual(self._metadata(partner)[0], self.env.user)
        self.assertNotEqual(self._metadata(partner)[1], OLD)

    def test_create_non_admin_is_ignored(self):
        partner = self.Partner.with_user(self.clerk).create(
            {"name": "New", "create_uid": self.author.id, "create_date": OLD}
        )
        self.assertEqual(self._metadata(partner)[0], self.clerk)
        self.assertNotEqual(self._metadata(partner)[1], OLD)

    def test_write(self):
        partners = self.env["res.partner"].create([{"name": "A"}, {"name": "B"}])
        partners.with_context(write_metadata=True).write(
            {"name": "Changed", "write_uid": self.editor.id, "write_date": OLD}
        )
        for partner in partners:
            self.assertEqual(partner.name, "Changed")
            self.assertEqual(self._metadata(partner)[2:], (self.editor, OLD))

    def test_write_only_metadata(self):
        partner = self.env["res.partner"].create({"name": "A"})
        partner.with_context(write_metadata=True).write(
            {"create_uid": self.author.id, "create_date": OLDER}
        )
        self.assertEqual(self._metadata(partner)[:2], (self.author, OLDER))

    def test_write_without_context(self):
        partner = self.env["res.partner"].create({"name": "A"})
        partner.write({"write_uid": self.editor.id, "write_date": OLD})
        self.assertEqual(self._metadata(partner)[2], self.env.user)

    def test_write_non_admin_is_ignored(self):
        partner = self.env["res.partner"].create({"name": "A"})
        partner.with_user(self.clerk).with_context(write_metadata=True).write(
            {"name": "B", "write_uid": self.editor.id, "write_date": OLD}
        )
        self.assertNotEqual(self._metadata(partner)[2], self.editor)
        self.assertNotEqual(self._metadata(partner)[3], OLD)

    def test_later_write_updates_write_metadata(self):
        partner = self.Partner.create(
            {"name": "Old", "write_uid": self.editor.id, "write_date": OLD}
        )
        partner.write({"name": "Changed"})
        partner.flush_recordset()
        self.assertEqual(self._metadata(partner)[2], self.env.user)
        self.assertNotEqual(self._metadata(partner)[3], OLD)

    def test_unknown_user(self):
        with self.assertRaises(ValidationError):
            self.Partner.create({"name": "Old", "create_uid": 999999999})

    def test_load(self):
        """The import converts names, XML IDs and ids of users."""
        self.env["ir.model.data"].create(
            {
                "module": "test_import_metadata",
                "name": "author",
                "model": "res.users",
                "res_id": self.author.id,
            }
        )
        cases = [
            ("create_uid", "Original Author"),
            ("create_uid/id", "test_import_metadata.author"),
            ("create_uid/.id", str(self.author.id)),
        ]
        for column, value in cases:
            with self.subTest(column=column):
                result = self.Partner.load(
                    ["name", column, "create_date"],
                    [["Loaded", value, "2016-01-02 03:04:05"]],
                )
                self.assertFalse(result["messages"], result["messages"])
                partner = self.env["res.partner"].browse(result["ids"])
                self.assertEqual(self._metadata(partner)[:2], (self.author, OLD))
