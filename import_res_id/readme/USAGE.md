Import messages, attachments or activities with a `res_external_id` column
holding the complete XML ID of the document, as `module.name`. The model and
the id of the document are set from it:

| body | message_type | res_external_id | attachment_ids/id |
|---|---|---|---|
| `<p>Called the customer</p>` | comment | `legacy.partner_42` | `legacy.attachment_7` |

| activity_type_id/id | summary | date_deadline | user_id/id | res_external_id |
|---|---|---|---|---|
| `mail.mail_activity_data_call` | Call back | 2026-12-01 | `base.user_admin` | `legacy.partner_42` |

The field can also be given to `create()` and `write()`, and is filled in
exports with the first XML ID of the document.

- An XML ID that does not exist stops the import with an error, instead of
  creating a message or attachment that is not linked to anything.
- The usual access rights apply to the document. Only administrators can
  move an existing message to another document.
- Import the attachments first, linked to the document with
  `res_external_id`, then the messages that refer to them with
  `attachment_ids/id`.

When importing a history, import the documents themselves with
`"mail_create_nolog": True` or `"tracking_disable": True` in the context, so
that Odoo does not add a *created* message of today next to the imported
messages. Messages keep the `date` and `author_id` of the import file. To also
keep their `create_uid` and `create_date`, use the `import_metadata` module.
