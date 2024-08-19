meta:
  id: wave_data
  file-extension: bin
  endian: le

seq:
  - id: num_hr_records
    type: u4
  - id: num_mid_records
    type: u4
  - id: num_peak_records
    type: u4

  - id: hr_records
    type: record
    repeat: expr
    repeat-expr: num_hr_records

  - id: mid_records
    type: record
    repeat: expr
    repeat-expr: num_mid_records

  - id: peak_records
    type: record
    repeat: expr
    repeat-expr: num_peak_records

types:
  record:
    seq:
      - id: identifier
        type: str
        encoding: ASCII
        size: 10
      - id: value
        type: f8
