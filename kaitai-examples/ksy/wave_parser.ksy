meta:
  id: test
  file-extension: test
  endian: le
  
seq:
  - id: lengths
    type: full_mid_peak_lens
  
  - id: f_data
    type: full_data

  - id: m_data
    type: mid_data
  
  - id: p_data
    type: peak_data
  
types:
  full_mid_peak_lens:
    seq:
      - id: full_len
        type: u4
      - id: mid_len
        type: u4
      - id: peak_len
        type: u4

  full_data:
    seq:
      - id: x_data
        type: f4
        repeat: expr
        repeat-expr: _root.lengths.full_len

      - id: y_data
        type: f4
        repeat: expr
        repeat-expr: _root.lengths.full_len
  
  mid_data:
    seq:
      - id: x_data
        type: f4
        repeat: expr
        repeat-expr: _root.lengths.mid_len

      - id: y_data
        type: f4
        repeat: expr
        repeat-expr: _root.lengths.mid_len
  
  peak_data:
    seq:
      - id: x_data
        type: f4
        repeat: expr
        repeat-expr: _root.lengths.peak_len

      - id: y_data
        type: f4
        repeat: expr
        repeat-expr: _root.lengths.peak_len