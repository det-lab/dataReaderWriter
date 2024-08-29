meta:
  id: cdms_v1
  endian: le
  
seq:
  
  - id: odb_hdr
    type: odb_info_header
    
  - id: event
    type: entry_block
    repeat: expr
    #repeat-expr: 17
    repeat-expr: 2401
    
  - id: odb_ftr
    type: odb_info_footer
  
    
types:

  odb_info_header:
    seq:
      - id: odb_hdr
        type: u2
      - id: unknown
        size: 10
      - id: odb_size
        type: u4
      - id: odb
        size: odb_size

  odb_info_footer:
    seq:
      - id: odb
        type: u2
      - id: unknown
        size: 10
      - id: odb_ftr_size
        type: u4
      - id: odb_ftr
        size: odb_ftr_size

  entry_block:
    seq:
      - id: midas_hdr
        type: midas_header
        
      - id: glob_hdr
        type: bank_header
        
      - id: empty_bank
        size: 0
        if: glob_hdr.all_banks_size == 0
        
      - id: bank_hdr
        type: bank32_header
        size: glob_hdr.all_banks_size
        if: glob_hdr.all_banks_size > 0
        
        
        
  midas_header:
    seq:
      - id: evt_id
        type: u2
        doc: |
          1 for triggered events, 2 for scaler events, 3 for HV events
      - id: trigger_mask
        type: u2
        doc: |
          Describes subtype of event
      - id: serial_number
        type: u4
        doc: |
          Starts at 0, increments for each event
      - id: time_stamp
        type: u4
      - id: evt_data_size
        type: u4
        doc: |
          Size of event excluding header
        
  bank_header:
    seq:
      - id: all_banks_size
        type: u4
        doc: |
          Size of following banks, including bank name
      - id: flags
        type: u4
        
        
  bank32_header:
    seq:
      - id: bank_name
        type: str
        size: 4
        encoding: utf-8
      - id: type
        type: u4
      - id: bank_size
        type: u4
      - id: data
        size: bank_size
        
  # Add after header when done      
  scdms_header:
  
    seq:
      - id: packed_event_size
        type: u4
      
      instances:
        trig_header:
          value: ((packed_event_size & 0xf0_00_00_00) >> 28)
      event_size:
          value: (packed_event_size & 0x0f_ff_ff_ff)
        
  