Import the original creation and last update user and date of records, the
`create_uid`, `create_date`, `write_uid` and `write_date` fields.

Odoo always sets these fields itself, and drops any value given for them. When
data is migrated from another system, the original author and dates are lost.
With this module, an administrator can keep them by importing with the
`write_metadata` key in the context.
