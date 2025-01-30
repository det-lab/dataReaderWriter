meta:
  id: soudan
  file-extension: soudan
  endian: le

seq:
  - id: file_hdr
    type: two_word_file_header
    
  - id: detector_hdr
    type: detector_config_header
    
  - id: hdrs
    type: header_list
    repeat: expr
    repeat-expr: detector_hdr.repeat_value
  
  - id: logical_rcrds
    type: logical_records

types:

  format_word:
    seq:
      - id: daq_major
        type: u1
      - id: daq_minor
        type: u1
      - id: data_format_major
        type: u1
      - id: data_format_minor
        type: u1
        
  two_word_file_header:
    seq:
      - id: endian_indicator
        size: 4
        doc: |
          le if '[4, 3, 2, 1]'
          be if '[1, 2, 3, 4]'
        
      - id: data_format
        type: format_word
        
  detector_config_header:
    seq:
      - id: header_num
        type: u4
        
      - id: config_record_len
        type: u4
        
    instances:
      repeat_value:
        value: (config_record_len / 72) + (config_record_len / 144)
        
  phonon_config_header:
    seq:
      - id: phonon_channel_config_record_len
        type: u4
      - id: detector_code
        type: s4
      - id: tower_num
        type: s4
      - id: post_amp_gain
        type: s4
      - id: qet_bias
        type: s4
      - id: squid_bias
        type: s4
      - id: squid_lockpoint
        type: s4
      - id: rtf_offset
        type: s4
      - id: variable_gain
        type: s4
      - id: delta_t
        type: s4
      - id: trigger_time
        type: s4
      - id: trace_len
        type: s4
        
  charge_config_header:
    seq:
      - id: charge_config_len
        type: u4
      - id: detector_code
        type: s4
      - id: tower_num
        type: s4
      - id: channel_post_amp
        type: s4
      - id: channel_bias
        type: s4
      - id: rtf_offset
        type: s4
      - id: delta_t
        type: s4
      - id: trigger_time
        type: s4
      - id: trace_len
        type: s4
        
  header_list:
    seq:
      - id: header_num
        type: u4
        
      - id: phonon_config
        type: phonon_config_header
        if: header_num == 0x10001
        
      - id: charge_config
        type: charge_config_header
        if: header_num == 0x10002
        
  event_header:
    seq:
      - id: event_header_word
        type: u4
      
      - id: event_size
        type: u4
        
    instances:
      event_identifier:
        value: (event_header_word >> 16) & 0xFFFF
        
    
      event_class:
        value: (event_header_word >> 8) & 0xF
        doc: |
          0x0: Raw
          0x1: Processed
          0x2: Monte Carlo
        
      event_category:
        value: (event_header_word >> 12) & 0xF
        doc: |
          0x0: Per Trigger
          0x1: Occasional
          0x2: Begin File Series
          0x3: Begin File
          0x4: End File
          0x5: End File Series
          0x6: Per Trigger w/ Selective Readout of Detectors that Cross Threshold
      
      event_type:
        value: (event_header_word & 0xFF)
        doc: |
          0x0: Wimp Search
          0x1: 60Co Calibration
          0x2: 60Co Low Energy Calibration
          0x3: Neutron Calibration
          0x4: Random Triggers
          0x5: Pulser Triggers
          0x6: Test
          0x7: Data Monitering Event
          0x8: 137Cs Calibration
          0x9: 133Ba Calibration
          0xa: Veto OR Multiplicity Trigger
          
  administrative_record:
    seq:
      - id: admin_len
        type: u4
        doc: |
          24 bytes
      - id: series_num_1
        type: u4
        doc: |
          LLYYMMDD
      - id: series_num_2
        type: u4
        doc: |
          HHMM
      - id: event_num_in_series
        type: u4
      - id: seconds_from_epoch
        type: u4
        doc: |
          Event time
          Epoch defined as Jan 1st 1904 for SUF (MAC artifact)
          Epoch defined as Jan 1st 1970 for Soudan
      - id: time_from_last_event
        type: u4
        doc: |
          Time in Milliseconds
      - id: live_time_from_last_event
        type: u4
        doc: |
          Time in Milliseconds
        
  trace_record:
    seq:
      - id: trace_len
        type: u4
      - id: trace_bookkeeping_header
        type: u4
        doc: |
          0x0000 0011
      - id: bookkeeping_len
        type: u4
      - id: digitizer_base_address
        type: u4
      - id: digitizer_channel
        type: u4
      - id: detector_code
        type: u4
      - id: timebase_header
        type: u4
        doc: |
          0x0000 0012
      - id: timebase_len
        type: u4
      - id: t0_in_ns
        type: s4
      - id: delta_t_ns
        type: u4
      - id: num_of_points
        type: u4
      - id: second_trace_header
        type: u4
        doc: |
          0x0000 0013
      - id: num_samples
        type: u4
        doc: |
          Should be a power of two
          (1024, 2048, 4096, etc)
      
  data_sample:
    seq:
      - id: data_selection
        type: u4
        
    instances:
      sample_a:
        value: (data_selection >> 16) & 0xFFFF
        
      sample_b:
        value: data_selection & 0xFFFF
        
  trace_data:
    seq:
      - id: trace_rcrd
        type: trace_record
        
      - id: sample_data
        type: data_sample
        repeat: expr
        repeat-expr: trace_rcrd.num_samples / 2
        
  soudan_history_buffer:
    seq:
      - id: history_buffer_len
        type: u4
      - id: num_time_nvt
        type: u4
      - id: time_nvt
        type: u4
        repeat: expr
        repeat-expr: num_time_nvt
      - id: num_veto_mask_words
        type: u4
      - id: time_n_minus_veto_mask
        type: u4
        repeat: expr
        repeat-expr: num_time_nvt * num_veto_mask_words
      - id: num_trigger_times
        type: u4
      - id: times
        type: u4
        repeat: expr
        repeat-expr: num_trigger_times
      - id: num_trigger_mask_words_per_time
        type: u4
      - id: times_minus_trigger_mask
        type: u4
        repeat: expr
        repeat-expr: num_trigger_mask_words_per_time * num_trigger_times
        
  gps_data:
    seq:
      - id: len
        type: u4
      - id: gps_year_day
        size: len_value
      - id: gps_status_hour_minute_second
        size: len_value
      - id: gps_microsecs_from_gps_second
        size: len_value
        
    instances:
      len_value:
        value: '(len > 0) ? 4 : 0'
        
  trigger_record_format:
    seq:
      - id: trigger_len
        type: u4
      - id: trigger_time
        type: u4
      - id: individual_trigger_mask
        type: u4
        repeat: expr
        repeat-expr: 6
        
  tlb_trigger_mask_record:
    seq:
      - id: tlb_len
        type: u4
      - id: tower_mask
        type: u4
        repeat: expr
        repeat-expr: 6
        
  detector_trigger_threshold_data:
    seq:
      - id: len_to_next_header
        type: u4
      - id: minimum_voltage_level
        type: u4
      - id: maximum_voltage_level
        type: u4
      - id: dynamic_range
        type: u4
      - id: tower_num
        type: u4
      - id: detector_codes
        type: u4
        repeat: expr
        repeat-expr: 6
      - id: operations_codes
        type: u4
        repeat: expr
        repeat-expr: 9
      - id: adc_values
        type: u4
        repeat: expr
        repeat-expr: 54
       
  detector_trigger_rates:
    seq:
      - id: len_to_next_header
        type: u4
      - id: clocking_interval
        type: u4
      - id: tower_num
        type: u4
      - id: detector_codes
        type: u4
        repeat: expr
        repeat-expr: 6
      - id: j_codes
        type: u4
        repeat: expr
        repeat-expr: 5
      - id: counter_values
        type: u4
        repeat: expr
        repeat-expr: 30
       
  veto_trigger_rates:
    seq:
      - id: len_to_next_header
        type: u4
      - id: clocking_interval
        type: u4
      - id: num_entries
        type: u4
      - id: detector_code
        type: u4
        repeat: expr
        repeat-expr: num_entries
      - id: counter_value_det_code
        type: u4
        repeat: expr
        repeat-expr: num_entries
        
  logical_records:
    seq:
      - id: event_hdr
        type: event_header
        
      - id: next_sect
        type: next_section
        repeat: expr
        repeat-expr: 10

  next_section:
    seq:
      - id: next_header
        type: u4
        enum: record_type
        
      - id: section
        type:
          switch-on: next_header
          cases:
            'record_type::administrative_record': administrative_record
            'record_type::trace_data': trace_data
            'record_type::soudan_history_buffer': soudan_history_buffer
            'record_type::gps_data': gps_data
            'record_type::trigger_record_format': trigger_record_format
            'record_type::tlb_trigger_mask_record': tlb_trigger_mask_record
            #'record_type::detector_trigger_threshold_data': detector_trigger_threshold_data
            'record_type::detector_trigger_rates': detector_trigger_rates
            'record_type::veto_trigger_rates': veto_trigger_rates
           
    enums:
      record_type:
        0x00000002: administrative_record
        0x00000011: trace_data
        0x00000021: soudan_history_buffer
        0x00000060: gps_data
        0x00000080: trigger_record_format
        0x00000081: tlb_trigger_mask_record
        # Documented header num for dttd and soudan buffer are identical
        #0x00000021: detector_trigger_threshold_data
        0x00000022: detector_trigger_rates
        0x00000031: veto_trigger_rates