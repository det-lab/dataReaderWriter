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
    
  - id: unknown384
    size: 384
    
  - id: group1
    type: entry_block_24
    
  - id: group2
    type: entry_block_192
    repeat: expr
    repeat-expr: 3
    
  - id: group3
    type: entry_block_168
    repeat: expr
    repeat-expr: 2
    
  - id: group4
    type: entry_block_192
    
  - id: group5
    type: entry_block_168
    
  - id: group6
    type: entry_block_192
    repeat: expr
    repeat-expr: 2
    
  - id: group7
    type: entry_block_168
  
  - id: group8
    type: entry_block_192
    
  - id: group9
    type: entry_block_168
    repeat: expr
    repeat-expr: 2
  
    
types:

  entry_block_24:
    seq:
      - id: midas_hdr
        type: midas_header
      - id: data
        size: midas_hdr.bank_size
      - id: unknown
        type: unknown_pad_24
        
  entry_block_192:
    seq:
      - id: midas_hdr
        type: midas_header
      - id: data
        size: midas_hdr.bank_size
      - id: unknown
        type: unknown_pad_192
  
  entry_block_168:
    seq:
      - id: midas_hdr
        type: midas_header
      - id: data
        size: midas_hdr.bank_size
      - id: unknown
        type: unknown_pad_168
    
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
      - id: bank_name
        type: str
        size: 4
        encoding: utf-8
      - id: type
        type: u4
      - id: bank_size
        type: u4
        
  unknown_pad_24:
    seq:
      - id: padding
        size: 24
        
  unknown_pad_168:
    seq:
      - id: padding
        size: 168
        
  unknown_pad_192:
    seq:
      - id: padding
        size: 192
        
