

meta:
  id: midas
  file-extension: mid
  endian: le
  ks-version: 0.8

  imports:
    - scdms

seq:

  - id: n_events
    type: event
    repeat: eos

types:

  event:
    seq:
      - id: event_header
        type: event_hdr

      - id: data_block
        type:
          switch-on: event_header.event_id
          cases:
            0x8000: odb_dump
            0x8001: odb_dump
            _: event_data


  # Header for each event in the file
  event_hdr:
    seq:
      - id: event_id
        type: u2
      - id: trigger_mask
        type: u2
      - id: serial_number
        type: u4
      - id: time_stamp
        type: u4
      - id: evt_data_size
        type: u4

  # probably just need the size of the odb dump for now, that comes from
  # the event header so we access that value by using the _parent attribute to
  # go up a level to the parent of odb_dump (event) and then back down into
  # the event_header
  odb_dump:
    seq:
      - id: odb
        size: _parent.event_header.evt_data_size


  event_data:
    seq:
      - id: bank_header
        type: bank_hdr

      - id: bank
        type:
          switch-on: (bank_header.flags & (1 << 4))
          cases:
            0: bank16
            _: bank32

  bank_hdr:
    seq:
      - id: all_bank_size
        type: u4
      - id: flags
        type: u4

  bank16:
    seq:
      - id: name
        type: str
        size: 4
        encoding: UTF-8

      - id: type
        type: u2

      - id: size
        type: u2

        # finally, the data portion of the bank is the scdms data as
        # defined in scdms.ksy
      - id: data
        type: scdms

  bank32:
    seq:
      - id: name
        type: str
        size: 4
        encoding: UTF-8

      - id: type
        type: u4

      - id: size
        type: u4

      - id: data
        type: scdms
