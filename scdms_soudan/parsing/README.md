# soudan_parser

## Overview

The files soudan_parser.py and scdms_soudan_parser.ipynb are for generating hdf5 files out of raw data created using the Super CDMS-Soudan data format. The main difference between the two files is in their format - scdms_soudan_parser.ipynb is broken up into different cells so that specific sections of the code can be tested independantly of each other. It also includes a cell after the parsing instructions to test the functionality of other modules, such as scdms_soudan/csv_metadata.py. The two files should otherwise be identical to one another.

## Raw Data Structure

The raw data exists in a binary data format which is then processed using the Construct module before being written to an hdf5 (Hierarchical Data Format) file designed for organizing and storing large amount of data. 

In hdf5, the data is further broken up across Groups (container structures to hold Datasets or other Groups), and Datasets (typed multidimensional arrays). The result is a hierarchical, filesystem-like file, which can be programmatically explored or viewed using an hdf5 viewer program. 

Using Construct, the raw data is sectioned into 4 main structures based off of existing documentation before the hdf5 file can be generated:
1. file_hdr

    Comprised of two 4-byte words: endian_indicator and data_format. endian_indicator captures 4 bytes which indicate if the file is written in little or big-endian format. The 4 bytes of data_format are DAQ major, DAQ minor, data-format major, and data-format minor. If the Soudan data version is 2.0, data-format major is 2 and data-format minor is 0. DAQ major is the major field in the version number of the daq, likewise for DAQ minor.
2. detector_hdr

    Comprised of the header_number (0x0001 0000), config_record_len (the length of the following section), and repeat_value, which is calculated from config_record_len and used to repeat the instructions of the next section. 
3. hdrs

    This is an array with a length determined by repeat_value of the header_number (either 0x0001 0001 for phonon channels or 0x0001 0002 for charge channels), and then either the phonon_config_header or charge_config_header respectively.
4. logical_rcrds

    The start of logical_rcrds is marked by the existence of a 4-byte Event Header Word. The first two bytes are the unique event identifier (0xA980), the next byte is split in half to find the 4 bit event_class and 4 bit event_category, with the last byte stating the event_size. 

    After this point, logical_rcrds reads the next header number to switch between any of the following options which will be elaborated on in the following section. Not all of the following options are always present in the raw data:
    * administrative_record 
    * trace_data
    * soudan_history_buffer
    * gps_data
    * trigger_record
    * tlb_trigger_mask_record
    * detector_trigger_rates
    * veto_trigger_rates

## logical_rcrds continued:

For the sake of completeness and readability, the data collected as logical_rcrds will be elaborated upon in this section in reference to the documentation provided by the collaboration.

### administrative_record
The Administrative record contains general information about each event. Each raw data file is uniquely identified using a Series Number as well as the relative times of events in the same series. It contains:
* admin_header (0x0000 0002)
* admin_len (24 bytes)
* series_number_1 (LLYYMMDD)
* series_number_2 (HHMM)
* event_number_in_series
* seconds_from_epoch
    
    An epoch is defined as 12am on Jan 1st 1904 for SUF (this is an artifact of Macs). For Soudan, the epoch is defined from the Unix Epoch, 12am on Jan 1st 1970.
* time_from_last_event (milliseconds)
* live_time_from_last_event (milliseconds)

### trace_data
This section is broken up into two main parts: trace_rcrds and sample_data.

trace_rcrds is composed of the following data:
* trace_header (0x0000 0011)
* trace_len 
* trace_bookkeeping_header (0x0000 0011)
* bookkeeping_len (12 bytes)
* digitizer_base_address
* digitizer_channel
* detector_code
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

The actual data of the event is then captured by sample_data, which is an array half the length of num_samples. data_selection collects 4 bytes, the first 2 of which are sample_a and the second two of which are sample_b. So despite the array being half the length of num_samples, the value refers to the total number of sample data.

### soudan_history_buffer


### gps_data


### trigger_record


### tlb_trigger_mask_record


### detector_trigger_rates


### veto_trigger_rates



## HDF5 File Structure

When creating the HDF5 file, there is one group for each of the four above sections, with each of those groups containing subgroups and/or datasets of the associated values, plus an additional series group which copies information directly relating to an event's trace data and data from each of the detectors for each event. 

### Series Group

The series group is named using series_number_1 and series_number_2 found in "logical_rcrds/admin_rcrd", where series_number is their concatenated values. The series group is then "S(series_number)" and contains data from every event in the uploaded raw data file, each in a group named "E(event_number)" with the event_number being collected from "logical_rcrds/admin_rcrd/admin_rcrd_group_[i]/event_number_in_series" where "i" iterates up from 0 for each individual event in the raw file. From there, each event group contains a further subgroup for every involved detector associated with the event. 

The detector group is named "det_code_(xxxyyyzzz)" where xxx, yyy, and zzz correspond respectively to the detector type, the detector number, and the channel number. In principle, there can be variation allowing for up to 999 options for each of the three values, but in practice detector type and channel number should not exceed a value of 11. 

Detector codes are collected under trace_rcrds (a subStruct of trace_data) and then processed with the function get_detector_code_info which is designed to take a 7 or 8 digit code and return the detector type (such as Blip/Flip/Veto/ZIP/Error/etc), whether or not the detector is set to record charge or phonon data (or if the data was Veto'd or contains an Error), and the detector number.