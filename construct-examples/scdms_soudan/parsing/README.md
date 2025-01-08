# Super CDMS-Soudan parsing code
**Created by: Adrian Fisher**

## Table of Contents:
- [Overview](#overview)
- [Raw Data Structure](#raw-data-structure)
- [hdrs details](#hdrs-details)
    - [charge_config_header](#charge_config_header)
    - [phonon_config_header](#phonon_config_header)
- [logical_rcrds details](#logical_rcrds-details)
    - [administrative_record](#administrative_record)
    - [trace_data](#trace_data)
    - [soudan_history_buffer](#soudan_history_buffer)
    - [gps_data](#gps_data)
    - [trigger_record](#trigger_record)
    - [tlb_trigger_mask_record](#tlb_trigger_mask_record)
    - [detector_trigger_threshold_data](#detector_trigger_threshold_data)
    - [detector_trigger_rates](#detector_trigger_rates)
    - [veto_trigger_rates](#veto_trigger_rates)
- [HDF5 File Structure](#hdf5-file-structure)
    - [Series Group](#series-group)

## Overview

The files `soudan_parser.py` and `scdms_soudan_parser.ipynb` are for generating `HDF5` files out of raw data created using the Super CDMS-Soudan data format. The main difference between the two files is in their format: `scdms_soudan_parser.ipynb` is broken up into different cells so that specific sections of the code can be tested independantly of each other. It also includes a cell after the parsing instructions to test the functionality of other modules, such as `scdms_soudan/csv_metadata.py`. `soudan_parser.py` should also avoid other testing convention such as print statements function tests. The two files should otherwise be identical to one another.

The codes are designed for researchers working with Super CDMS-Soudan data.

```
Dependencies:
- construct>=2.10.70
- h5py>=3.11.0
```

## Raw Data Structure

The raw data exists in a binary data format which is processed using python's `Construct` module before being written to an `HDF5` (Hierarchical Data Format) file designed for organizing and storing large amount of data using python's `h5py` module.

Using `HDF5`, the data is further broken up across Groups (container structures to hold Datasets or other Groups), and Datasets (typed multidimensional arrays). The result is a hierarchical, filesystem-like file, which can be programmatically explored, or can be viewed using an `HDF5` viewer program. 

Using `Construct`, the raw data is parsed into 4 main structures based off of existing documentation before the `HDF5` file can be generated:
1. `file_hdr`

    Comprised of two 4-byte "words": `endian_indicator` and `data_format`. `endian_indicator` captures 4 bytes which indicate if the file is written in little or big-endian format. Each of the 4 bytes of `data_format` are `daq_major`, `daq_minor`, `data_format_major`, and `data_format_minor`. If the Soudan data version is 2.0, `data_format_major` is 2 and `data_format_minor` is 0. `daq_major` is the major field in the version number of the daq, likewise for `daq_minor`.
2. `detector_hdr`

    Comprised of the identifying `header_number` (0x0001 0000), `config_record_len` (the length of the following section), and `repeat_value`, which is calculated from `config_record_len` and used to repeat the instructions of the next section. 
3. `hdrs`

    This is an array with a length (determined by `repeat_value`) of a variable `header_number` (either 0x0001 0001 for phonon channels or 0x0001 0002 for charge channels), and then either the `phonon_config_header` or `charge_config_header` based on the value of `header_number` (see [hdrs continued](#hdrs-continued)). This means that for each charge or phonon channel, there will be a new group containing the configuration information of that respective channel until there are a `repeat_value` number of `*_config_header`s.
4. `logical_rcrds`

    The start of `logical_rcrds` is marked by the existence of a 4-byte Event Header Word. The first two bytes are the unique event identifier (0xA980), while the next byte is split in half to find the 4 bit `event_class` and 4 bit `event_category`, with the last byte stating the `event_size`. 

    After this point, `logical_rcrds` reads the following header number to switch between any of the following options (see [logical_rcrds continued](#logical_rcrds-continued)). Not all of the following options are neccesarrily present in the raw data:
    * administrative_record 
    * trace_data
    * soudan_history_buffer
    * gps_data
    * trigger_record
    * tlb_trigger_mask_record
    * detector_trigger_rates
    * veto_trigger_rates

Each raw data file should only have one instance of sections 1-3, after which logical_rcrds should repeat until the end of the file for every event.

## `hdrs` details:

As mentioned previously, `hdrs` contains the header information from all of the charge and phonon detectors which were used for a given event. There should be twice as many phonon channels as charge channels, and there are twice as many bins for phonon trace data as there are for charge trace data. The separate config headers collect the following data:

### `charge_config_header`

* charge_config_len (32 bytes)
* detector_code (see [trace_data](#trace_data))
* tower_number 
* channel_post_amp

    Charge channel post-amp (driver) gain * 100
* channel_bias [uV]
* rtf_offset [uV]
* delta_t [ns]
* trigger_time (time of trigger in trace [ns])
* trace_len (samples)

### `phonon_config_header`

* phonon_config_len (44 bytes)
* detector_code (see [trace_data](#trace_data))
* tower_number
* post_amp_gain

    Phonon post-amp (driver) gain * 100
* qet_bias

    Phonon QET bias * 100 [pA]
* squid_bias

    Phonon SQUID bias * 100 [pA]
* squid_lockpoint

    Phonon SQUID lockpoint * 100 [pA]
* rtf_offset [uV]
* variable_gain (tunes SQUID bandwidth)
* delta_t [ns]
* trigger_time (time of trigger in trace [ns])
* trace_len (samples)

## `logical_rcrds` details:

Each of the sections of `logical_rcrds` is collected either between event headers or until the end of the file. As in for one event, logical_rcrds could contain all of the following sections or only some.

### `administrative_record`

The administrative record contains general information about each event. Each raw data file is identified using a Series Number as well as the relative times of events in the same series. It contains:
* admin_header (0x0000 0002)
* admin_len (24 bytes)
* series_number_1 (LLYYMMDD)

    Where LL represents a location and YYMMDD represents the date that the series began. LL = [0: SUF, 1: Soudan, 2: UCB, 3: CWRU, 6: Queens, 7: U of Minn]
* series_number_2 (HHMM)

    HHMM represents the time at which the series began. A series which started at 4:30 pm on Jan 15th 2010 at Soudan would thus have the Series Number 01100115_1630
* event_number_in_series
* seconds_from_epoch
    
    An epoch is defined as 12am on Jan 1st 1904 for SUF (this is an artifact of Macs). For Soudan, the epoch is defined from the Unix Epoch, 12am on Jan 1st 1970.
* time_from_last_event (milliseconds)
* live_time_from_last_event (milliseconds)

### `trace_data`

This section is broken up into two main parts: `trace_rcrds` and `sample_data`.

`trace_rcrds` is composed of the following data:
* trace_header (0x0000 0011)
* trace_len 
* trace_bookkeeping_header (0x0000 0011)
* bookkeeping_len (12 bytes)
* digitizer_base_address
* digitizer_channel
* detector_code

    Takes the form of xxxyyyzzz, where xxx is the detector type, yyy is the detector number, and zzz is the channel number.
* timebase_header (0x0000 0012)
* timebase_len (12 bytes)
* t0_in_ns

    Beginning of the trace relative to the time of the trigger for that digitizer module
* delta_t_ns

    1/(digitization rate)
* num_of_points
* second_trace_header (0x0000 0013)
* num_samples

(num_of_points and num_samples should be equivalent.)

The actual data of the event is then captured by `sample_data`, which is an array half the length of `num_samples`. `data_selection` collects 4 bytes, the first 2 of which are `sample_a` and the second two of which are `sample_b`. So despite the array being half the length of `num_samples`, the value refers to the total number of sample data.

### `soudan_history_buffer`

* history_buffer_header (0x0000 0021)
* history_buffer_len
* num_time_nvt (number of veto times, nvt)
* time_nvt
    
    This is an array which repeats as many times as stated by num_time_nvt
* num_veto_mask_words

    Number of veto mask words per time (nvw)
* time_n_minus_veto_mask

    This is an array which repeats (num_time_nvt * num_veto_mask_words) times
* num_trigger_times (ntt)
* trigger_times

    This is an array which repeats num_trigger_times. The value has units of microseconds.
* num_trigger_mask_words (ntw)
* trig_times_minus_trig_mask

    This is an array which repeats (num_trigger_times * num_trigger_mask_words). 

### `gps_data`

* tlb_mask_header (0x0000 0060)
* length

    This value can be 0 - if so, the following values do not exist.
* gps_year_day
* gps_status_hour_minute_second
* gps_microseconds_from_gps_second

The last three values are in BCD (binary-coded decimal) format of the form:

GPS year/day                  0xyyyy dddd

GPS Status/hour/minute/second 0xS0hh mmss

GPS 0.1us's from GPS second   0xuuuu uuuu

For instance, for an event occuring on the 320th day of 2005 at 11:15:26 AM exactly 0.2 seconds after the turn of the GPS second, the 3 GPS words would be printed in hex as:

0x2005 0320

0x0011 1526

0x0200 0000 (2,000,000 counts of 0.1 microsecond units)

**Note:** As of Jan 3rd 2025, these values are not coverted from decimal in the parsing code. To use these values, convert them from decimal to hex.

### `trigger_record`

* trigger_header (0x0000 0080)
* trigger_len
* trigger_time (always 0)
* individual_trigger_masks

    This is an array which repeats 6 times

### `tlb_trigger_mask_record`

* tlb_mask_header (0x0000 0081)
* tlb_len
* tower_mask

    This is an array which repeats 6 times
### `detector_trigger_threshold_data`

The trigger thresholds and phonon offsets for each tower are read out by a 64 channel scanning ADC module (VMIVME3128). This structure guides the data format of this section:

* threshold_header (0x0000 0021)
* len_to_next_header (in bytes)
* minimum_voltage_level (in V)
* maximum_voltage_level (in V)
* dynamic_range (14 bits = 0x3fff)
* tower_number 
* detector_codes

    Array of 6 values taking the form xyy - using the same form as in trace data
* operations_codes

    Array of 9 values taking the form p00j
    | p value              | j value                         |
    | ---------------------| --------------------------------|
    | 1: phonon offset     | 1-4 corresponding to phonon A-D |
    | 2: trigger threshold | 1: Qhigh                        |
    |                      | 2: Qlow                         |
    |                      | 3: Phigh                        |
    |                      | 4: Plow                         |
    |                      | 5: Whisper                      |
* adc_values

    Array of 54 (6*9) values, det code 1: operation code 1, det code 1: operation code 2... det code 6: operation code 9

### `detector_trigger_rates`

* detector_trigger_header (0x0000 0022)
* len_to_next_header (in bytes)
* clocking_interval (in microseconds)
* tower_number
* detector_codes

    Array of 6 detector codes in the same format as in `detector_trigger_threshold_data`
* j_codes

    Array of 5 j-codes in the same format as in `detector_trigger_threshold_data`
* counter_values

    Array of 30 (6*5) values, det code 1: j-code 1, det code 1: j-code 2... det code 6: j-code 5
### veto_trigger_rates

* veto_trigger_header (0x0000 0031)
* len_to_next_header (in bytes)
* clocking_interval (in microseconds)
* num_entries
* detector_code

    Array of num_entries codes in the same xyy format as in `detector_trigger_rates` and `detector_trigger_threshold_data`. For veto panels, x=3.
* counter_value_det_code

    Array of `num_entries` counter values from detector code 1 to detector code num_entries.

## HDF5 File Structure

When creating the `HDF5` file, there is one group for each of the sections referred to in [Raw Data Structure](#raw-data-structure), with each of those groups containing subgroups and/or datasets of the associated values. There is then an additional series group which copies information directly relating to an event's trace data and data from each of the detectors for each event to allow for easier access to said data.

For the data which is contained in arrays, such as the data contained in `hdrs` or `logical_rcrds`, the subgroups are named iteratively starting from 0.

For example, if one is attempting to access the trigger time of the third charge_config header, the path would be `root > hdrs > charge_config > charge_config_2 > trigger_time`

### Series Group

The series group is named using `series_number_1` and `series_number_2` found in `logical_rcrds/admin_rcrd`. The series group is then "S(`series_number`)" where `series_number` is the concatenated values of `series_number_1` and `series_number_2`. 

The group contains data from every event in the uploaded raw data file, each in a group named "E(`event_number`)" with the `event_number` being collected from `logical_rcrds/admin_rcrd/admin_rcrd_group_[i]/event_number_in_series` where `i` iterates from 0 for each individual event in the raw file. From there, each event group contains a further subgroup for every involved detector associated with the event. 

The detector groups are named as `det_code_(xxxyyyzzz)` where `xxx`, `yyy`, and `zzz` correspond respectively to the `detector_type`, the `detector_number`, and the `channel_number`. In principle, there can be variation allowing for up to 999 options for each of the three values, but in practice `detector_type` and `channel_number` should not exceed a value of 11.

Detector codes are collected under `trace_rcrds` (see [trace_data](#trace_data)) and then processed with the function `get_detector_code_info`, designed to take a 7 or 8 digit code and return information such as the detector type (Blip/Flip/Veto/ZIP/Error/etc), whether or not the detector is set to record charge or phonon data (or if the data was Veto'd or contains an Error), and the detector number.

After being processed, the `det_code_(xxxyyyzzz)` group is given the datasets `detector_number`, `detector_type`, `trace_type` (such as charge/phonon/etc), and finally the `trace` data which was collected by the detector. 