# CSV Metadata functions
** Created by Adrian Fisher **

## Table of contents:
- [Overview](#overview)
- [Basic Usage](#basic-usage)
    - [Trace data](#trace-data)
    - [Cut data](#cut-data)

## Overview:
The file `csv_metadata` contains functions which can be used to save specific data from parsed `HDF5` files which were created using raw data from the Super CDMS-Soudan format and `soudan_parser.py`. The functions contained therein use the metadata files provided by [the Super CDMS Team](https://gitlab.com/supercdms/Analysis/cdmslite-run3-cuts-output). As stated there:

> The file ID_CDMSliteR3.csv contains the series number and event number for the low background data of CDMSlite Run3.
> Each cut file in the repository has corresponding cut outputs.
> The row content is preserved, meaning each row in the ID_CDMSliteR3.csv file corresponds to cut outputs in individual files.

As such, the functions of `csv_metadata.py` search the parsed `HDF5` files to find their series numbers and event numbers. Select data can then be collected and outputted as trace or cut `HDF5` files. Trace data includes data about the detectors and the data from the event, and cut data includes the true or false statements from the files mentioned above. 

The functions are designed for researchers working with Super CDMS-Soudan data.

```
- Dependencies:
- h5py>= 3.11.0
- pandas>= 2.2.3
- os
- re
- time
```

## Basic Usage

Several of the functions of `csv_metadata` rely on the `ID_CDMSliteR3.csv` file, which is loaded as a pandas dataframe with the `load_id_file(cdms_ids_file_path)` function. Using that dataframe, called `cdms_ids` in the functions, series and event numbers are matched by index against the other cut data files to either locate the relevant `True/False` value(s) or to find which cut data files said event is `True` or `False` on.

The other functions center around collecting one or more event's detector info and trace data. The data is grabbed directly from the parsed `HDF5` files.

For both uses, it is important to first find the correct series and event numbers. This can be done using either the function `get_series_num` or `get_series_and_event_numbers`. As can be expected, the first function uses a parsed `HDF5` file to return its series number, while the second uses the file to grab the series number and every event number in the file. The event numbers are returned as a list. If a function takes a `parsed_hdf5_file_path`, it is also using one of these functions for its purposes.

Many functions have a boolean `is_test` option, which if true, shortens the number of events that are tested and prints information about the progress of the function.

### Trace data

The function `get_event_det_code_data` takes a `parsed_hdf5_file_path` and a given event number, returning a dictionary with a unique key for each detector that measured the event and the values of the `detector_number`, `detector_type` (such as `Blip`, `Flip`, `iZIP`, etc), `trace_type` (such as `Charge`, `Phonon`, `Veto`, or `Error`), and the actual `trace` data from that specific detector.

The functions `get_single_event_metadata`, and `get_series_trace_data` use this dictionary to create `HDF5` groups from each detector code and then datasets of the above values on each of those groups. 

### Cut data

The function `get_event_cut_data` uses a loaded panda dataframe as `cut_data` and the index of an event number as found in `cdms_ids`, returning the boolean value of the event in said `cut_data` file, or `None` if the event somehow doesn't have a value. 

The functions `get_single_event_metadata` and `get_series_cut_data` use this function to iterate through each of the `cut_data` files in a folder, collecting their values for the given event or given events and creating `HDF5` files. In the generated files, each of the `cut_data` file names and values are stored as datasets in the group set by the event number.

The functions `find_valid_series_events`, `find_overlapping_bool` and `fetch_events_from_dict` are the last functions of `csv_metadata`. They all also deal with the `cut_data` files, and as such all require the `cdms_ids` dataframe, but they are working in the other direction - using `cut_data` bools to find events. 

Given a specific `cut_data_file_path`, `find_valid_series_events` will return two dictionaries: one whose keys and values are the series numbers and a respective list of event numbers that are registered as `True` in the file, and a second dictionary of the same for the `False` values. 

`find_overlapping_bool` is designed to take the path to the `cut_data_csv_folder` and two lists of `cut_data` filenames: a 'true' list, on which the user is only looking for events that are true, and a 'false' list, on which the user is only looking for events that are false. For instance, if one is looking for every restricted random event with a good phonon start time which isn't on a bad series, they could pass in the lists:

```
true_list = [
    'out_bg-restricted_Random_CDMSliteR3.csv',
    'cut_output_bg-restricted_GoodPhononStartTime_CDMSliteR3.csv'
]

false_list = [
    'out_bg-restricted_IsBadSeries_CDMSliteR3.csv'
]
```

The function will return a dictionary as above of every event which intersects the two lists.

The final function then uses either of those dictionaries to create an `HDF5` file for the cut data, and another file for the trace data, for each of the events in the dictionary.