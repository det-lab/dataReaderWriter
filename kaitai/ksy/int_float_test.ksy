meta:

  id: int_float_test
  file-extension: int_float_test
  endian: le
  
seq:
  - id: data_entry
    type: int_float_array
    repeat: expr
    repeat-expr: 8
    
types:

  int_float_test:
  
    seq:
  
      - id: int_field
        type: u4
      
      - id: float_field
        type: f8
      
  int_float_array:
  
    seq:
    
     - id: entries
       type: int_float_test