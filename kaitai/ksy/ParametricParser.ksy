meta:
  id: kv_pairs
  file-extension: bin
  
seq:
  - id: short_pairs
    type: kv_pair(3)
    repeat: expr
    repeat-expr: 0x100
  - id: long_pairs
    type: kv_pair(8)
    repeat: expr
    repeat-expr: 0x100
types:
  kv_pair:
    params:
      - id: len_key
        type: u2
    seq:
      - id: key
        size: len_key
        type: str
        encoding: ASCII
        
      - id: value
        type: strz
        encoding: ASCII