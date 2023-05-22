meta:
  id: test
  endian: le
  
enums:

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
  
seq:
  - id: odb_hdr
    type: u2
  - id: unknown
    size: 10
  - id: odb_size
    type: u4
  - id: odb
    size: odb_size
    
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
    
  - id: scdms_hdr
    type: scdms_header
  - id: trigger_blk
    type: trigger_block
    repeat: expr
    repeat-expr: scdms_hdr.total_triggers
  - id: scdms_ftr
    type: scdms_footer
  


types:

  scdms_header:

    seq:
      - id: packed
        type: u4

    instances:

      overall_header:
        value: ((packed & 0xf0_00_00_00) >> 28)

      total_triggers:
        value: (packed & 0x00_00_0f_ff)

      format_version:
        value: ((packed & 0x0f_ff_f0_00) >> 12)
  
  trigger_block:
    seq: 
    - id: event_hdr
      type: event_header
    - id: num_primitive_hdr
      type: num_primitive_header
    - id: primitive_blk
      type: primitive_block
      repeat: expr
      repeat-expr: num_primitive_hdr.num_primitives
    - id: n_detectors
      type: detectors
    - id: detector_blk
      type: detector_block
      repeat: expr
      repeat-expr: n_detectors.detectors_in_event
    - id: sdu_primitive_hdr
      type: sdu_primitive_header
    - id: sdu_primitive_blk
      type: sdu_primitive_block
      repeat: expr
      repeat-expr: sdu_primitive_hdr.num_sdu_primitives
    - id: num_sdu_hdr
      type: num_sdu_header
    - id: sdu_blk
      type: sdu_block
      #if: num_sdu_hdr.num_sdu != 0
      repeat: expr
      repeat-expr: num_sdu_hdr.num_sdu
  
  event_header:
  
    seq:
      - id: packed_event_size
        type: u4
      - id: trigger_id
        type: u4
      - id: event_number
        type: u4
      - id: packed_type
        type: u4
      - id: global_timestamp_low
        type: u4
      - id: global_timestamp_high
        type: u4
      - id: packed_poll_end
        type: u4
      - id: poll_time_fraction
        type: u4
        
    instances:
    
      # Values parsed from packed_event_size
      trig_header:
        value: ((packed_event_size & 0xf0_00_00_00) >> 28)
      event_size:
        value: (packed_event_size & 0x0f_ff_ff_ff)
        
      # Values parsed from packed_type
      trigger_type:
        value: (packed_type & 0x00_00_00_0f)
        enum: trigger_types
      readout_bitmask:
        value: ((packed_type & 0xff_ff_ff_00) >> 8)
        
      # Values parsed from packed_poll_end
      poll_cycle_end_time:
        value: (packed_poll_end & 0x00_00_ff_ff)
        
  num_primitive_header:
    seq:
      - id: packed_primitive_num
        type: u4
      - id: entry_length
        type: u4
      
    instances:
      # Values parsed from packed_primitive_num
      num_primitives:
        value: (packed_primitive_num & 0x0f_ff_ff_ff)
      prim_header:
        value: ((packed_primitive_num & 0xf0_00_00_00) >> 28)
    
  primitive_block:
    seq:
      - id: packed_primitive
        type: u4
      - id: rt_issue_time
        type: u4
      - id: rt_run_time_fraction_packed
        type: u4
      - id: prim_trig_time
        type: u2
      - id: rt_run_time
        type: u2
      - id: trigger_mask_packed
        type: u4
      - id: trig_word
        type: u2
      - id: prim_blank
        type: u2
      - id: peak_amplitude
        type: u4
    
    instances:
      # Values parsed from packed_primitive
      trig_status:
        value: ((packed_primitive & 0x00_00_f0_00) >> 12)
      index:
        value: (packed_primitive & 0x00_00_00_03)
      det_id:
        value: ((packed_primitive & 0x00_00_03_fc) >> 2)
      pileup:
        value: ((packed_primitive & 0x00_00_0c_00) >> 10)
      prim_dcrc_header:
        value: ((packed_primitive & 0xf0_00_00_00) >> 28)
        
      # Values parsed from rt_run_time_fraction_packed
      rt_run_time_fraction:
        value: (rt_run_time_fraction_packed & 0x00_ff_ff_ff)
  
      # Values parsed from trigger_mask_packed
      trig_mask: 
        value: ((trigger_mask_packed & 0xff_00_00_00) >> 24)
      trig_time_frac: 
        value: (trigger_mask_packed & 0x00_ff_ff_ff)

  detectors: 
    seq:
      - id: n_detectors_packed
        type: u4
        
    instances:
      detectors_in_event:
        value: (n_detectors_packed & 0x0f_ff_ff_ff)

      num_det_header:
        value: ((n_detectors_packed & 0xf0_00_00_00) >> 28)
        
  detector_block:
    seq:
      - id: detector_hdr
        type: detector_header
      - id: readout_hdr
        type: readout_header
      - id: num_channels_hdr
        type: num_channels_header
      - id: channel_blk
        type: channel_block
        repeat: expr
        repeat-expr: num_channels_hdr.num_channels
        
  detector_header:
    seq:
      - id: detector_hdr_packed
        type: u4
      - id: dcrc1_serial_nbr
        type: u1
      - id: dcrc1_version
        type: u1
      - id: dcrc2_serial_nbr
        type: u1
      - id: dcrc2_version
        type: u1
    
    instances:
      detector_type:
        value: ((detector_hdr_packed & 0x0f_ff_fc_00) >> 10)
      index:
        value: (detector_hdr_packed & 0x00_00_00_03)
      det_id:
        value: ((detector_hdr_packed & 0x00_00_03_fc) >> 2)
      detector_header:
        value: ((detector_hdr_packed & 0xf0_00_00_00) >> 28)
        
  readout_header:
    seq:
      - id: readout_hdr_packed_1
        type: u4
      - id: readout_hdr_packed_2
        type: u4
      - id: waveform_read_start_time
        type: u2
      - id: waveform_read_end_time
        type: u2
      - id: waveform_read_start_time_fraction
        type: u4
      - id: waveform_read_end_time_fraction
        type: u4
        
    instances:
      readout_header:
        value: ((readout_hdr_packed_1 & 0xf0_00_00_00) >> 28)
      readout_status:
        value: ((readout_hdr_packed_1 & 0x0f_ff_00_00) >> 16)
      series_time:
        value: (readout_hdr_packed_1 & 0x00_00_ff_ff)
        
      has_thermometry_readout:
        value: ((readout_hdr_packed_2 & 0x10_00_00_00) >> 31)
      series_time_fraction:
        value: (readout_hdr_packed_2 & 0x00_00_ff_ff)
  
  num_channels_header:
    seq:
      - id: num_channels_packed
        type: u4
        
    instances:
      channels_header:
        value: ((num_channels_packed & 0xf0_00_00_00) >> 28)
      num_channels:
        value: (num_channels_packed & 0x0f_ff_ff_ff)
  
  channel_block:
    seq:
      - id: channel_packed
        type: u4
      - id: num_pre_pulse_samples
        type: u4
      - id: num_on_pulse_samples
        type: u4
      - id: num_post_pulse_samples
        type: u4
      - id: sample_rate
        type: u2
      - id: downsample_factor
        type: u2
      - id: sample
        type: u2
        repeat: expr
        repeat-expr: num_pre_pulse_samples + num_on_pulse_samples + num_post_pulse_samples
    
    instances:
      channel_flag:
        value: ((channel_packed & 0xf0_00_00_00) >> 28)
      pre_trigger_offset:
        value: ((channel_packed & 0x0f_ff_ff_c0) >> 7)
      channel_num:
        value: ((channel_packed & 0x00_00_00_3c) >> 2)
      has_baseline_control:
        value: ((channel_packed & 0x00_00_00_02) >> 1)
      channel_type:
        value: (channel_packed & 0x00_00_00_01)
        
  sdu_primitive_header:
    seq:
      - id: sdu_num_primitive_packed
        type: u4
      - id: sdu_entry_length
        type: u4
        
    instances:
      sdu_header:
        value: ((sdu_num_primitive_packed & 0xf0_00_00_00) >> 28)
      
      num_sdu_primitives:
        value: (sdu_num_primitive_packed & 0x07_ff_ff_ff)
      
      has_sdu_data:
        value: ((sdu_num_primitive_packed & 0x01_00_00_00) >> 27)
        
  sdu_primitive_block:
    seq:
      - id: sdu_block_header
        type: u4
      - id: rt_issue_ut
        type: u4
      - id: rt_run_time_fraction_packed
        type: u4
      - id: trigger_time
        type: u2
      - id: rt_run_time
        type: u2
      - id: trigger_time_fraction_packed
        type: u4
      - id: trigger_word
        type: u2
      - id: blank
        type: u4
      - id: peak_amplitude
        type: u2
        
    instances:
      rt_run_time_fraction:
        value: (rt_run_time_fraction_packed & 0x00_ff_ff_ff)
      
      trigger_time_fraction:
        value: (trigger_time_fraction_packed & 0x00_ff_ff_ff)
        
  num_sdu_header:
    seq: 
      - id: num_sdu_packed
        type: u4
        
    instances:
      num_sdu:
        value: (num_sdu_packed & 0x0f_ff_ff_ff)
      num_sdu_flag:
        value: ((num_sdu_packed & 0xf0_00_00_00) >> 28)
          
  sdu_block:
    seq:
      - id: sdu_readout_header_packed
        type: u4
      - id: sdu_series_time_fraction_packed
        type: u4
      - id: sdu_read_start_time
        type: u2
      - id: sdu_read_end_time
        type: u2
      - id: sdu_read_start_time_fraction
        type: u4
      - id: sdu_read_end_time_fraction
        type: u4
      - id: sdu_num_channels_header_packed
        type: u4
      - id: sdu_channel_blk
        type: sdu_channel_block
        repeat: expr
        repeat-expr: num_sdu_channels
    
    instances:
      sdu_readout_flag:
        value: ((sdu_readout_header_packed & 0xf0_00_00_00) >> 28)
      sdu_readout_status:
        value: ((sdu_readout_header_packed & 0x0f_ff_00_00) >> 16)
      sdu_series_time:
        value: (sdu_readout_header_packed & 0x00_00_ff_ff)
      sdu_series_time_fraction:
        value: (sdu_readout_header_packed & 0x00_ff_ff_ff)
        
      num_sdu_channels:
        value: (sdu_num_channels_header_packed & 0x0f_ff_ff_f)
      num_sdu_channels_flag:
        value: ((sdu_num_channels_header_packed & 0xf0_00_00_00) >> 28)
        
  sdu_channel_block:
    seq:
      - id: sdu_channel_header_packed
        type: u4
      - id: sdu_num_samples
        type: u4
      - id: blank
        type: u2
      - id: sample_rate
        type: u2
        doc: kHz
      - id: sdu_channel_sample
        type: u2
        repeat: expr
        repeat-expr: sdu_num_samples
        
    instances:
      sdu_channel_flag:
        value: ((sdu_channel_header_packed & 0xf0_00_00_00) >> 28)
      sdu_pre_trigger_offset:
        value: ((sdu_channel_header_packed & 0x0f_ff_ff_c0) >> 7)
      sdu_channel_type:
        value: ((sdu_channel_header_packed & 0x00_00_00_38) >> 3)
      sdu_channel_num:
        value: (sdu_channel_header_packed & 0x00_00_00_07)
        
  scdms_footer:
    seq:
      - id: preceeding_triggers_packed
        type: u4
    
    instances:
      preceeding_triggers_flag:
        value: ((preceeding_triggers_packed & 0xf0_00_00_00) >> 28)
      preceeding_triggers_num:
        value: (preceeding_triggers_packed & 0x0f_ff_ff_ff)