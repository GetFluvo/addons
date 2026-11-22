Import with `write_metadata` in the context, as a user of the
*Administration / Settings* group, and add any of the `create_uid`,
`create_date`, `write_uid` and `write_date` columns. For example with
`load()` through JSON-RPC or XML-RPC:

```python
models.execute_kw(
    db, uid, password, "res.partner", "load",
    [["name", "create_uid", "create_date"],
     [["Azure Interior", "Marc Demo", "2016-01-02 03:04:05"]]],
    {"context": {"write_metadata": True, "tz": "UTC"}},
)
```

The user columns accept what any many2one column of an import accepts:

- `create_uid`: the name of the user
- `create_uid/id`: the XML ID of the user
- `create_uid/.id`: the database id of the user

The dates are in the `YYYY-MM-DD HH:MM:SS` format. Like any date of an import,
`load()` reads them in the timezone of the context, or else of the importing
user, and stores them in UTC. Pass `"tz": "UTC"` in the context to import UTC
dates unchanged. Empty cells keep the value Odoo sets.

The context key also works for `create()` and `write()` called directly, with
user ids or records and datetimes or strings.

Without the context key, or for other users, the columns are ignored as without
this module, and the import does not fail.

Odoo posts a *created* message in the chatter of every new record, with the
date of the import and the importing user as author. For historical data,
suppress it with one of these context keys of Odoo, next to `write_metadata`:

- `"mail_create_nolog": True`: no *created* message.
- `"tracking_disable": True`: no *created* message, no tracking of field
  changes, and no automatic followers.
