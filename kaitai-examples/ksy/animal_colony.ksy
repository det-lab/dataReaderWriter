meta:
  id: colony
  file-extension: col
  endian: le

seq:
  - id: animal_entry
    type: animal_array
    repeat: expr
    repeat-expr: 8
    
  - id: colony_entry
    type: colony_array
    repeat: eos
    
types:
  animal_array:
    seq:
      - id: legs
        type: u4
        
      - id: animal
        type: str
        encoding: ascii
        size: 10
        
      - id: lifespan
        type: f8
        
  colony_array:
    seq:
      - id: name
        type: str
        encoding: ascii
        size: 10
        
      - id: int
        type: u4
        
      - id: birthday
        type: str
        encoding: ascii
        size: 10