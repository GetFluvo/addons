# Copyright 2026 Strategic Efficiency B.V.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from collections import defaultdict

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools import SQL

USER_FIELDS = ("create_uid", "write_uid")
DATE_FIELDS = ("create_date", "write_date")
METADATA_FIELDS = USER_FIELDS + DATE_FIELDS


class Base(models.AbstractModel):
    _inherit = "base"

    @api.model_create_multi
    def create(self, vals_list):
        if not self._import_metadata_enabled():
            return super().create(vals_list)
        vals_list = [dict(vals) for vals in vals_list]
        metadata_list = [self._import_metadata_pop(vals) for vals in vals_list]
        records = super().create(vals_list)
        records._import_metadata_write(metadata_list)
        return records

    def write(self, vals):
        if not self._import_metadata_enabled():
            return super().write(vals)
        vals = dict(vals)
        metadata = self._import_metadata_pop(vals)
        result = super().write(vals)
        self._import_metadata_write([metadata] * len(self))
        return result

    @api.model
    def _import_metadata_enabled(self):
        """Whether the metadata in the values must be written.

        Only with ``write_metadata`` in the context, for an administrator.
        For other users the values are dropped by the ORM, as without this
        module.
        """
        return bool(
            self._log_access
            and self.env.context.get("write_metadata")
            and self.env.user._is_system()
        )

    @api.model
    def _import_metadata_pop(self, vals):
        """Remove the metadata from ``vals`` and return it, normalized.

        Users are ids or ``res.users`` records, dates are datetimes or
        strings in the server format, in UTC. Empty values are ignored.
        """
        metadata = {}
        for fname in METADATA_FIELDS:
            value = vals.pop(fname, None)
            if not value:
                continue
            if fname in USER_FIELDS:
                if isinstance(value, models.BaseModel):
                    value = value.id
                user = self.env["res.users"].browse(int(value))
                if not user.with_context(active_test=False).exists():
                    raise ValidationError(
                        self.env._(
                            "%(field)s: user with id %(id)s does not exist.",
                            field=fname,
                            id=value,
                        )
                    )
                metadata[fname] = user.id
            else:
                metadata[fname] = fields.Datetime.to_datetime(value)
        return metadata

    def _import_metadata_write(self, metadata_list):
        """Write the metadata of each record of ``self`` in the database.

        The ORM sets the metadata of every record it writes, so the pending
        updates are flushed first. A later write in the same transaction,
        for instance a recomputation, sets ``write_uid`` and ``write_date``
        again.
        """
        groups = defaultdict(list)
        for record, metadata in zip(self, metadata_list, strict=True):
            if metadata:
                groups[tuple(sorted(metadata.items()))].append(record.id)
        if not groups:
            return
        self.flush_recordset()
        for items, ids in groups.items():
            self.env.cr.execute(
                SQL(
                    "UPDATE %s SET %s WHERE id IN %s",
                    SQL.identifier(self._table),
                    SQL(", ").join(
                        SQL("%s = %s", SQL.identifier(fname), value)
                        for fname, value in items
                    ),
                    tuple(ids),
                )
            )
        self.invalidate_recordset(list({f for items in groups for f, _v in items}))
