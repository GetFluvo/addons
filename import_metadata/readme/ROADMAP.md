- `write_uid` and `write_date` are set again by any later write to the record,
  including writes done by Odoo itself later in the same transaction, for
  instance a recomputation of a stored field. Import them last, or in a
  separate import of the same records.
