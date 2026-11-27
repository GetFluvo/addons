Adds a *Document XML ID* field, `res_external_id`, to messages
(`mail.message`), attachments (`ir.attachment`) and activities
(`mail.activity`), to link them to their document by the XML ID of that
document.

Messages, attachments and activities point to their document with a model
and a database id, which an import file cannot know. With this field, chatter
messages, attachments and activities, such as to-dos and calls with a deadline
and an assignee, can be imported for records imported earlier.
