meta:
  id: scdms
  #file-extension: NOTE - The scdms format is encapsulated
  # within a midas file so it won't have its own extension
  endian: le
  # license:
  ks-version: 0.8

seq:

  - id: scdms_hdr
    type: scdms_header

  - id: n_triggers
    type:
      switch-on: scdms_hdr.format_version
      cases:
        1: v_one_trigger
        2: v_two_trigger
    repeat: expr # repeat for the number of triggers read
    repeat-expr: scdms_hdr.total_triggers

  - id: scdms_footer
    type: trailer


enums:

  headers:
    0x9:
      id: scdms_hdr
    0x5:
      id: trigger_hdr
    0x7:
      id: primitive_hdr
    0x6:
      id: prim_dcrc_hdr
    0x3:
      id: detector_hdr
    0x2:
      id: dcrc_hdr
    0x4:
      id: readout_hdr
    0x0:
      id: channel_hdr
    0x1:
      id: waveform_hdr
    0x8:
      id: trailer

  trigger_types:
    1:
      id: physics # trigger based on L1 primitives
    2:
      id: borr    # begin of run randoms
    3:
      id: irr     # in run randoms
    4:
      id: eorr    # end of run randoms
    5:
      id: bcr     # baseline control randoms
    6:
      id: borts   # begin of run test signal
    7:
      id: eorts   # end of run test signal

types:

  scdms_header:

    seq:
      - id: packed
        type: u4

    instances:

      overall_header:
        value: ((packed & 0xf0_00_00_00) >> 28)
        enum: headers

      total_triggers:
        value: (packed & 0x00_00_0f_ff)

      format_version:
        value: ((packed & 0x0f_ff_f0_00) >> 12)

  v_one_trigger:
    seq:
      - id: trigger_meta
        type: v_one_trig_meta

      - id: n_primitives
        type: primitive
        repeat: expr # repeat for number of primitives
        repeat-expr: trigger_meta.num_primitives

      - id: packed
        type: u4

      - id: n_detectors
        type: detector
        repeat: expr # repeat for the number of detectors
        repeat-expr: detectors_in_event

    instances:
      detectors_in_event:
        value: (packed & 0x0f_ff_ff_ff)

      det_header:
        value: ((packed & 0xf0_00_00_00) >> 28)
        enum: headers

  v_two_trigger:
    seq:
      - id: trigger_meta
        type: v_two_trig_meta

      - id: n_primitives
        type: primitive
        repeat: expr # repeat for number of primitives
        repeat-expr: trigger_meta.num_primitives

      - id: packed
        type: u4

      - id: n_detectors
        type: detector
        repeat: expr # repeat for the number of detectors
        repeat-expr: detectors_in_event

    instances:
      detectors_in_event:
        value: (packed & 0x0f_ff_ff_ff)

      det_header:
        value: ((packed & 0xf0_00_00_00) >> 28)
        enum: headers

  v_one_trig_meta:
    seq:

      - id: packed_1
        type: u4

      - id: trigger_id
        type: u4

      - id: trigger_type
        type: u4
        enum: trigger_types

      - id: global_timestamp_low
        type: u4

      - id: global_timestamp_high
        type: u4

      - id: packed_2
        type: u4

      - id: length_of_entry
        type: u4
        doc: Length of Entry in Bytes

    instances:
      event_size:
        value: (packed_1 & 0x0f_ff_ff_ff)

      trig_header:
        value: ((packed_1 & 0xf0_00_00_00) >> 28)
        enum: headers

      num_primitives:
        value: (packed_2 & 0x0f_ff_ff_ff)

      prim_header:
        value: ((packed_1 & 0xf0_00_00_00) >> 28)
        enum: headers

  v_two_trig_meta:
    seq:

      - id: packed_1
        type: u4

      - id: trigger_id
        type: u4

      - id: event_number
        type: u4

      - id: packed_2
        type: u4

      - id: global_timestamp_low
        type: u4

      - id: global_timestamp_high
        type: u4

      - id: packed_3
        type: u4

      - id: length_of_entry
        type: u4
        doc: Length of Entry in Bytes


    instances:

      # Values parsed from packed_1
      trig_header:
        value: ((packed_1 & 0xf0_00_00_00) >> 28)
        enum: headers
      event_size:
        value: (packed_1 & 0x0f_ff_ff_ff)

      # Values parsed from packed_2
      trigger_type:
        value: (packed_2 & 0x00_00_00_0f)
        enum: trigger_types
      readout_bitmask:
        value: ((packed_2 & 0xff_ff_ff_00) >> 8)

      # Values parsed from packed_3
      num_primitives:
        value: (packed_3 & 0x0f_ff_ff_ff)
      prim_header:
        value: ((packed_3 & 0xf0_00_00_00) >> 28)
        enum: headers


  primitive:
    seq:

      - id: packed_1
        type: u4

      - id: ut
        type: u4

      - id: packed_2
        type: u4

      - id: rt_run_time
        type: u2
      - id: trig_time
        type: u2

      - id: packed_3
        type: u4

      - id: peak_amplitude
        type: u2
      - id: trig_word
        type: u2

    instances:

      # Values parsed from packed_1
      index:
        value: (packed_1 & 0x00_00_00_03)
      det_id:
        value: ((packed_1 & 0x00_00_03_fc) >> 2)
      pileup:
        value: ((packed_1 & 0x00_00_0c_00) >> 10)
      trig_status:
        value: ((packed_1 & 0x00_00_f0_00) >> 12)
      prim_dcrc_header:
        value: ((packed_1 & 0xf0_00_00_00) >> 28)
        enum: headers

      # Value parsed from packed_2
      rt_time_fraction:
        value: (packed_2 & 0x00_ff_ff_ff)

      # Values parsed from packed_3
      trig_time_fraction:
        value: (packed_3 & 0x00_ff_ff_ff)
      mask_pairs:
        value: ((packed_3 & 0xff_00_00_00) >> 24)


  detector:
    seq:

      - id: detector_meta
        type: det_meta

      - id: n_channels
        type: channel
        repeat: expr # repeat for the number of chanels
        repeat-expr: detector_meta.num_channels_to_follow

  det_meta:
    seq:

      - id: packed_1
        type: u4

      - id: dcrc0_version
        type: u1

      - id: dcrc0_serial_num
        type: u1

      - id: dcrc1_version
        type: u1

      - id: dcrc1_serial_num
        type: u1

      - id: packed_2
        type: u4

      - id: packed_3
        type: u4

      - id: packed_4
        type: u4

    instances:

      # Values parsed from packed_1
      index:
        value: (packed_1 & 0x00_00_00_03)

      det_id:
        value: ((packed_1 & 0x00_00_03_fc) >> 2)

      det_type:
        value: ((packed_1 & 0x0f_ff_fc_00) >> 10)

      dcrc_header:
        value: ((packed_1 & 0xf0_00_00_00) >> 28)
        enum: headers

      # Values parsed from packed_2
      series_time:
        value: (packed_2 & 0x00_00_ff_ff)

      readout_status:
        value: ((packed_2 & 0x0f_ff_00_00) >> 16)

      readout_header:
        value: ((packed_2 & 0xf0_00_00_00) >> 28)
        enum: headers

      # Values parsed from packed_3
      series_time_fraction:
        value: (packed_3 & 0x00_ff_ff_ff)

      # Values parsed from packed_4
      num_channels_to_follow:
        value: (packed_4 & 0x0f_ff_ff_ff)

      channel_header:
        value: ((packed_4 & 0xf0_00_00_00) >> 28)
        enum: headers

  channel:
    seq:

      - id: packed
        type: u4

      - id: n_pre_pulse_samples
        type: u4  # 4 byte unsigned integer
      - id: n_on_pulse_samples
        type: u4
      - id: n_post_pulse_samples
        type: u4
      - id: sample_rate_low
        type: u2
      - id: sample_rate_high
        type: u2
      - id: sample
        type: u2
        repeat: expr
        repeat-expr: n_pre_pulse_samples + n_on_pulse_samples + n_post_pulse_samples

    instances:

      ch_type:
        value: (packed & 0x00_00_00_03)

      ch_num:
        value: ((packed & 0x00_00_00_3c) >> 2)

      pre_trigger_offset:
        value: ((packed & 0x0f_ff_ff_c0) >> 6)

      chnl_header:
        value: ((packed & 0xf0_00_00_00) >> 28)
        enum: headers

  trailer:
    seq:

      - id: packed
        type: u4

    instances:

      n_preceeding_triggers:
        value: (packed & 0x0f_ff_ff_ff)
      trailer_header:
        value: ((packed & 0xf0_00_00_00) >> 28)
        enum: headers
