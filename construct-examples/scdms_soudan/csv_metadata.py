import h5py
import pandas as pd
import os
import re
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
from functools import reduce
# Suppress unneccessary 3D package warning
import warnings
warnings.filterwarnings('ignore', message='Unable to import Axes3D')

def load_id_file(cdms_ids_file_path):
    cdms_ids = pd.read_csv(cdms_ids_file_path, header = None, names = ['index', 'series-event'])
    # split series-event column into 'series_number' and 'event_number'
    cdms_ids[['series_number', 'event_number']] = cdms_ids['series-event'].str.split('-', expand = True)
    # drop redundant column
    cdms_ids = cdms_ids.drop('series-event', axis=1)
    return cdms_ids

def get_series_num(parsed_hdf5_file_path):
    """
    Find the series number of any parsed hdf5 file.
    """
    with h5py.File(parsed_hdf5_file_path, 'r') as f:
        series_pattern = r'S(\d+)'
        for group_name in f:
            series_match = re.match(series_pattern, group_name)
            if series_match:
                series_number = series_match.group(1)
    return series_number

def get_series_and_event_numbers(parsed_hdf5_file_path):
    """
    Collect all event numbers in a given parsed hdf5 file
    """
    event_numbers = []
    with h5py.File(parsed_hdf5_file_path, 'r') as f:
        event_pattern = r'E(\d+)'
        series_number = get_series_num(parsed_hdf5_file_path)
        series_group = f[f'S{series_number}']
        for group_name in series_group:
            event_match = re.match(event_pattern, group_name)
            if event_match:
                event_number = event_match.group(1)
                event_numbers.append(event_number)
    return series_number, event_numbers

def get_event_det_code_data(parsed_hdf5_file_path, series_number, event_number):
    """"
    Create a dictionary of trace data for a given series event.
    """
    base_path = f'S{series_number}/E{event_number}/'
    det_code_dict = {}
    with h5py.File(parsed_hdf5_file_path, "r") as parsed_f:
        base_group = parsed_f[base_path]
        for detector_group in base_group.keys():
            try:
                detector_data_path = f'{base_path}{detector_group}'
                detector_data = parsed_f[detector_data_path]

                # Initialize a dictionary for this detector
                det_data = {}
                for det_data_group_name in detector_data.keys():
                    det_data[det_data_group_name] = detector_data[det_data_group_name][()]
                det_code_dict[detector_group] = det_data
            except Exception as e:
                print(f'Error copying group {detector_group}:\n{e}')
    
    return det_code_dict

def get_event_cut_data(cdms_ids, cut_data_file, series_number, event_number):
    """
    Find bool values for all cut data types for a given event.
    """
    se_index = cdms_ids.loc[
        (cdms_ids['series_number'] == series_number) & (cdms_ids['event_number'] == event_number)
        ].index
    se_index = se_index[0]
    # Load cut_data_file
    cut_data = pd.read_csv(cut_data_file, header=None, names=['bool value'])
    cut_data = cut_data.astype(bool)
    # Match index on cut_data_file
    try:
        value_at_event = cut_data.iloc[se_index].item()
    except:
        value_at_event = None

    return value_at_event

def get_single_event_metadata(cdms_ids, event_number, parsed_hdf5_file_path, cut_data_csv_folder, trace_output_file_path, cut_output_file_path, is_test=False):
    """
    Create a trace output and cut output file for a single event.
    """
    series_number = get_series_num(parsed_hdf5_file_path)
    with h5py.File(trace_output_file_path, 'w') as trace_out:
        if is_test:
            print(f'Collecting trace data..')
        uid_group = trace_out.create_group('UID')
        series_group = uid_group.create_group(f'S{series_number}')
        event_group = series_group.create_group(f'E{event_number}')
        det_code_dict = get_event_det_code_data(parsed_hdf5_file_path, series_number, event_number)
        for det_code, datasets in det_code_dict.items():
            det_code_group = event_group.create_group(det_code)
            for dataset_name, data in datasets.items():
                det_code_group.create_dataset(dataset_name, data=data)
        if is_test:
            print(f'Trace data saved.')
    
    with h5py.File(cut_output_file_path, 'w') as cut_out:
        if is_test:
            print(f'Collecting cut data...')
        uid_group = cut_out.create_group('UID')
        series_group = uid_group.create_group(f'S{series_number}')
        event_group = series_group.create_group(f'E{event_number}')
        for cut_file in os.listdir(cut_data_csv_folder):
            if '.csv' not in cut_file:
                continue
            if 'small' in cut_file:
                continue
            if 'ID' in cut_file:
                continue
            if is_test:
                print(f'Fetching for {cut_file}')

            cut_file_path = os.path.join(cut_data_csv_folder, cut_file)
            data_name = cut_file[:-4] # cut off .csv for naming
            try:
                value_at_event = get_event_cut_data(cdms_ids, cut_file_path, series_number, event_number)
            except:
                # Saving as None without quotes creates an anonymous dataset
                value_at_event = 'None'
            try:
                event_group.create_dataset(data_name, data=value_at_event)
            except Exception as e:
                print(f"Error saving cut data for S{series_number}/E{event_number}:\n{e}")

def get_series_trace_data(parsed_file_folder, trace_output_file_path, is_test=False):
    """
    Create a trace output file for all events 
    available in a folder of parsed hdf5 files.
    """
    with h5py.File(trace_output_file_path, 'w') as trace_out:
        if is_test:
            print(f'Collecting trace data...')
        uid_group = trace_out.create_group('UID')
        series_group_created = False # track if there's already a series_group

        for parsed_file in os.listdir(parsed_file_folder):

            # Skip folders
            if not os.path.isfile(os.path.join(parsed_file_folder, parsed_file)):
                continue
            
            if parsed_file.endswith('_parsed.hdf5'):
                parsed_file = os.path.join(parsed_file_folder, parsed_file)
                series_number, event_numbers = get_series_and_event_numbers(parsed_file)
                if not series_group_created:
                    series_group = uid_group.create_group(f"S{series_number}")
                    series_group_created = True
                
                if is_test:
                    event_numbers = event_numbers[:9]
                    #print(f'Event numbers: {event_numbers}')

                for event_number in event_numbers:
                    try:
                        event_group = series_group.create_group(f'E{event_number}')

                        det_code_dict = get_event_det_code_data(parsed_file, series_number, event_number)
                        
                        for det_code, datasets in det_code_dict.items():
                            det_code_group = event_group.create_group(det_code)
                            for dataset_name, data in datasets.items():
                                det_code_group.create_dataset(dataset_name, data=data)

                    except Exception as e:
                        print(f'Error generating trace output for event {event_number}:\n{e}')
        if is_test:
            print(f'Completed collecting test trace data for series {series_number}.')

def get_series_cut_data(cdms_ids, parsed_hdf5_file_path, cut_data_csv_folder, cut_output_file_path, is_test=False):
    """
    Create a cut output file for all events 
    available in a folder of parsed hdf5 files.
    """
    # Find series number
    series_number = get_series_num(parsed_hdf5_file_path)
    se_indices = cdms_ids.loc[
        (cdms_ids['series_number'] == series_number)
    ].index.to_list()
    if is_test:
        se_indices = se_indices[:9]
    with h5py.File(cut_output_file_path, 'w') as cut_out:
        uid_group = cut_out.create_group('UID')
        series_group = uid_group.create_group(f'S{series_number}')
        for cut_file in os.listdir(cut_data_csv_folder):
            if '.csv' not in cut_file:
                continue
            if 'small' in cut_file:
                continue
            if 'ID' in cut_file:
                continue
            cut_file_path = os.path.join(cut_data_csv_folder, cut_file)
            data_name = cut_file[:-4] # cut off .csv for naming
            for index in se_indices:
                event_number = cdms_ids.loc[cdms_ids['index'] == index, 'event_number'].values[0]
                if f'E{event_number}' not in series_group:
                    event_group = series_group.create_group(f'E{event_number}')
                else:
                    event_group = series_group[f'E{event_number}']
                try:
                    value_at_event = get_event_cut_data(cdms_ids, cut_file_path, series_number, event_number)
                except:
                    value_at_event = ''
                try:
                    event_group.create_dataset(data_name, data=value_at_event)
                except Exception as e:
                    print(f'Error saving {data_name} for {event_number}:\n{e}')

def get_series_full_metadata(cdms_ids, parsed_file_folder, cut_data_csv_folder, trace_output_file_path, cut_output_file_path, is_test=False):
    """
    Use all parsed files in a folder to generate cut and trace outputs
    for every event in the series.
    """
    with h5py.File(trace_output_file_path, 'w') as trace_out:
        if is_test:
            print(f'Collecting trace data...')
        uid_group = trace_out.create_group('UID')
        series_group_created = False # track if there's already a series_group

        for parsed_file in os.listdir(parsed_file_folder):

            # Skip folders
            if not os.path.isfile(os.path.join(parsed_file_folder, parsed_file)):
                continue
            
            if parsed_file.endswith('_parsed.hdf5'):
                parsed_file = os.path.join(parsed_file_folder, parsed_file)
                series_number, event_numbers = get_series_and_event_numbers(parsed_file)
                if not series_group_created:
                    series_group = uid_group.create_group(f"S{series_number}")
                    series_group_created = True
                
                if is_test:
                    event_numbers = event_numbers[:9]
                    #print(f'Event numbers: {event_numbers}')

                for event_number in event_numbers:
                    try:
                        event_group = series_group.create_group(f'E{event_number}')

                        det_code_dict = get_event_det_code_data(parsed_file, series_number, event_number)
                        
                        for det_code, datasets in det_code_dict.items():
                            det_code_group = event_group.create_group(det_code)
                            for dataset_name, data in datasets.items():
                                det_code_group.create_dataset(dataset_name, data=data)

                    except Exception as e:
                        print(f'Error generating trace output for event {event_number}:\n{e}')
        if is_test:
            print(f'Completed collecting test trace data for series {series_number}.')

    if is_test:
        #Only use the first 10 lines for testing
        cdms_ids = cdms_ids.head(10)
        print(f'Collecting cut data...')
    with h5py.File(cut_output_file_path, 'w') as cut_out:
        uid_group = cut_out.create_group('UID')
        series_group_created = False
        for parsed_file in os.listdir(parsed_file_folder):
            if parsed_file.endswith('_parsed.hdf5'):
                try:
                    parsed_file = os.path.join(parsed_file_folder, parsed_file)
                    series_number, event_numbers = get_series_and_event_numbers(parsed_file)
                    if not series_group_created:
                        series_group = uid_group.create_group(f'S{series_number}')
                        series_group_created = True
                except Exception as e:
                    print(f'Error getting series and event numbers:\n{e}')
                if is_test:
                    event_numbers = event_numbers[:9]
                for event_number in event_numbers:
                    event_group = series_group.create_group(f'E{event_number}')
                    if is_test:
                        print(f'Getting event {event_number} cut data...')

                    for cut_file in os.listdir(cut_data_csv_folder):
                        if '_small' in cut_file:
                            continue
                        if  'ID' in cut_file:
                            continue
                        if '.csv' not in cut_file:
                            continue
                        cut_file_path = os.path.join(cut_data_csv_folder, cut_file)
                        try:
                            if is_test:
                                value_at_event = get_event_cut_data(cdms_ids, cut_file_path, series_number, event_number, is_test=True)
                            else:
                                value_at_event = get_event_cut_data(cdms_ids, cut_file_path, series_number, event_number, is_test=False)
                            event_group.create_dataset(cut_file, data=value_at_event)
                        except:# Exception as e:
                            event_group.create_dataset(cut_file, data='Null')
                            #print(f'Error saving {cut_file} for event {event_number}:\n{e}')
                    if is_test:
                        print(f'Data saved.\n')
            else:
                continue
            print(f'Finished {parsed_file}.')
        if is_test:
            print(f'Completed collecting test cut data for series {series_number}')

def find_overlapping_bool(cdms_ids, cut_data_csv_folder, true_list, false_list, is_test=False):
    """
    Querie for series/events on cut bools by providing lists for true and false cuts.
    """
    # Populate with all true events and find where they match
    true_event_indices = []
    if is_test:
        print(f'Looking for only TRUE events...')
    for cut_data_file in true_list:
        cut_data_file_path = os.path.join(cut_data_csv_folder, cut_data_file)
        cut_data = pd.read_csv(cut_data_file_path, header=None, names=['bool value'])
        cut_data = cut_data.astype(bool)
        if is_test:
            cut_data = cut_data.head(50)

        # Extract indices of true events
        true_indices = cut_data.index[cut_data['bool value']].tolist()
        true_event_indices.append(true_indices)
        if is_test:
            print(f'True at: {true_indices}')
    shared_true_indices = list(reduce(set.intersection, map(set, true_event_indices)))
    if is_test:
        print(f'Shared true indices:\n{shared_true_indices}')

    false_event_indices = []
    if is_test:
        print(f'Looking for only FALSE events...')
    for cut_data_file in false_list:
        cut_data_file_path = os.path.join(cut_data_csv_folder, cut_data_file)
        cut_data = pd.read_csv(cut_data_file_path, header=None, names=['bool value'])
        cut_data = cut_data.astype(bool)
        if is_test:
            cut_data = cut_data.head(50)

        # Extract indices of false events
        false_indices = cut_data.index[~cut_data['bool value']]
        if is_test:
            print(f'False at: {false_indices}')
        false_event_indices.append(false_indices)
    shared_false_indices = list(reduce(set.intersection, map(set, false_event_indices)))
    if is_test:
        print(f'Shared false indices:\n{shared_false_indices}')
    
    # Find overlap between the two groups
    all_shared_indices = []
    all_shared_indices.append(shared_true_indices)
    all_shared_indices.append(shared_false_indices)
    overlapping_indices = list(reduce(set.intersection, map(set, all_shared_indices)))
    overlapping_indices = sorted(overlapping_indices)
    if is_test:
        print(f'Overlapping indices:\n{overlapping_indices}')
    
    selected_rows = cdms_ids.iloc[overlapping_indices]
    print(selected_rows)

def find_valid_series_events(cut_data_file_path, cdms_ids, is_test=False):
    """
    Given a .csv cut data file, return two dictionaries,
    one of True series-event pairs and another of False series-event pairs
    """
    if is_test:
        #Only use the first 10 lines for testing
        cdms_ids = cdms_ids.head(10)

    # Load cut_data_file
    if is_test:
        cut_data_file_path = pd.read_csv(cut_data_file_path, header=None, names=['bool']).head(10)
    else:
        cut_data_file_path = pd.read_csv(cut_data_file_path, header=None, names=['bool'])

    # Filter for valid rows (where 'bool' = 1)
    valid_rows = cdms_ids.loc[cut_data_file_path['bool'] == 1]
    invalid_rows = cdms_ids.loc[cut_data_file_path['bool'] == 0]

    # Group by series_number, event_number as lists
    series_and_true_events = (
        valid_rows.groupby('series_number')['event_number']
        .apply(list)
        .to_dict()
    )
    
    series_and_false_events = (
        invalid_rows.groupby('series_number')['event_number']
        .apply(list)
        .to_dict()
    )

    if is_test:
        print('Valid series and events:')
        if series_and_true_events == {}:
            print('None')
        for series, events in series_and_true_events.items():
            print(f'Series: {series}, Num true events: {len(events)}')
        print(f'{series_and_true_events}')

        print('Invalid series and events:')
        if series_and_false_events == {}:
            print('None')
        for series, events in series_and_false_events.items():
            print(f'Series: {series}, Num false events: {len(events)}')
        print(f'{series_and_false_events}')

    else:
        try:
            first_valid_series, first_valid_event_list = next(iter(series_and_true_events.items()))
            print(f'First valid series: {first_valid_series}')
            print(f'First 10 valid events: {first_valid_event_list[0:10]}')
        except Exception as e:
            print(f"Failed to form valid series/event lists:\n{e}")

        try:
            first_invalid_series, first_invalid_event_list = next(iter(series_and_false_events.items()))
            print(f'First invalid series: {first_invalid_series}')
            print(f'First 10 invalid events: {first_invalid_event_list[0:10]}')
        except Exception as e:
            print(f"Failed to form invalid series/event lists:\n{e}")

    return series_and_true_events, series_and_false_events
