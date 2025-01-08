meta:
  id: record_list
  endian: le

types:
  record:
    seq:
      - id: name
        type: strz
        encoding: ASCII
      - id: age
        type: u4

params:
  - id: num_records
    doc: "Number of records in the list"
    type: u4

seq:
  - id: num_records_in_file
    type: u4
  - id: records
    type: record
    repeat: expr
    repeat-expr: _root.num_records