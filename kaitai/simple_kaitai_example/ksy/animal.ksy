

meta:
  id: animal
  endian: le
  ks-version: 0.8

seq:

  - id: entry
    type: animal_entry
    repeat: eos

types:

  animal_entry:
    seq:
      - id: str_len
        type: u1

      - id: species
        type: str
        size: str_len
        encoding: UTF-8

      - id: age
        type: u1

      - id: weight
        type: u2
