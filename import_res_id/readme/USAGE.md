Import messages or attachments with a `res_external_id` column holding the
complete XML ID of the document, as `module.name`. The model and the id of
the document are set from it:

| body | message_type | res_external_id | attachment_ids/id |
|---|---|---|---|
| `<p>Called the customer</p>` | comment | `legacy.partner_42` | `legacy.attachment_7` |

The field can also be given to `create()` and `write()`, and is filled in
exports with the first XML ID of the document.

- An XML ID that does not exist stops the import with an error, instead of
  creating a message or attachment that is not linked to anything.
- The usual access rights apply to the document. Only administrators can
  move an existing message to another document.
- Import the attachments first, linked to the document with
  `res_external_id`, then the messages that refer to them with
  `attachment_ids/id`.
