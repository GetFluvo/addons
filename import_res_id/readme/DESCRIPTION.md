Adds a *Document XML ID* field, `res_external_id`, to messages
(`mail.message`) and attachments (`ir.attachment`), to link them to their
document by the XML ID of that document.

Messages and attachments point to their document with a model name and a
database id, which an import file cannot know. With this field, chatter
messages and attachments can be imported for records imported earlier.
