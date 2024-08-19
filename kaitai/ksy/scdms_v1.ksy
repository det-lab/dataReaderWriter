meta:
  id: cdms_v1
  endian: le
  
seq:
  - id: odb_hdr
    type: u2
  - id: unknown
    size: 10
  - id: odb_size
    type: u4
  - id: odb
    size: odb_size
  - id: midas_hdr
    type: midas_header
  - id: midas_bank_hdr
    type: midas_bank_header
  - id: data
    size: midas_bank_hdr.bank_size
  - id: midas_bank_hdr2
    type: midas_bank_header
  - id: data2
    size: midas_bank_hdr2.bank_size
  - id: midas_bank_hdr3
    type: midas_bank_header_16bit
  - id: data3
    size: midas_bank_hdr3.bank_size
  - id: midas_bank_hdr4
    type: midas_bank_header


types:

  entry_block:
    seq:
      - id: midas_hdr
        type: midas_header
        

  midas_header:
    seq:
      - id: evt_id
        type: u2
      - id: trigger_mask
        type: u2
      - id: serial_number
        type: u4
      - id: time_stamp
        type: u4
      - id: evt_data_size
        type: u4
      - id: all_banks_size
        type: u4
      - id: flags
        type: u4
        
  midas_bank_header:
    seq:
      - id: bank_name
        type: str
        size: 4
        encoding: utf-8
      - id: type
        type: u4
      - id: bank_size
        type: u4

  midas_bank_header_16bit:
    seq:
      - id: bank_name
        type: str
        size: 4
        encoding: utf-8
      - id: type
        type: u4
      - id: bank_size
        type: u4
      - id: padding
        type: u4