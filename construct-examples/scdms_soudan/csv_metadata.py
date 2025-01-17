import h5py
import pandas as pd
import os
import re
from functools import reduce
import time

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

def get_event_det_code_data(parsed_hdf5_file_path, event_number):
    """"
    Create a dictionary of trace data for a given series event.
    """
    series_number = get_series_num(parsed_hdf5_file_path)
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

def get_event_cut_data(se_index, cut_data):
    """
    Find bool value for a cut data file on a given event.
    """
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
    index = cdms_ids.loc[
        (cdms_ids['series_number'] == series_number) & (cdms_ids['event_number'] == event_number), 'index'
        ].values[0]
    with h5py.File(trace_output_file_path, 'w') as trace_out:
        if is_test:
            print(f'Collecting trace data..')
        uid_group = trace_out.create_group('UID')
        series_group = uid_group.create_group(f'S{series_number}')
        event_group = series_group.create_group(f'E{event_number}')
        det_code_dict = get_event_det_code_data(parsed_hdf5_file_path, event_number)
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
            cut_file_path = os.path.join(cut_data_csv_folder, cut_file)
            cut_file_path = os.path.join(cut_data_csv_folder, cut_file)
            cut_data = pd.read_csv(cut_file_path, header=None, names=['bool value'])
            cut_data = cut_data.astype(bool)
            data_name = cut_file[:-4] # cut off .csv for naming
            if is_test:
                print(f'Fetching for {data_name}...')
            try:
                value_at_event = get_event_cut_data(index, cut_data)
            except:
                # Saving as None without quotes creates an anonymous dataset
                value_at_event = 'None'
                if is_test:
                    print(f'Missing data at event: {event_number}')
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
            test_number = 15
            print(f'Collecting trace data for {test_number} events in every file...')
        uid_group = trace_out.create_group('UID')
        series_group_created = False # track if there's already a series_group
        # Find how long it takes on average to get trace data for a number of events
        all_times = []
        max_num_events = []
        for parsed_file in os.listdir(parsed_file_folder):
            start_time = time.time()
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
                    num_of_events = len(event_numbers)
                    max_num_events.append(num_of_events)
                    event_numbers = event_numbers[:test_number]

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
                end_time = time.time()
                if is_test:
                    seconds_per_event = (end_time - start_time)/test_number
                    all_times.append(seconds_per_event)
        if is_test:
            average_time_per_event = sum(all_times) / len(all_times)
            max_num_events = sum(max_num_events)
            max_average_seconds = max_num_events * average_time_per_event
            print(f'This series has {max_num_events} events. It would take around {max_average_seconds:.2f} seconds, or {max_average_seconds/60:.2f} minutes to get trace data for all of them.')

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
    num_indices = len(se_indices)
    if is_test:
        test_number = 100
        print(f'Total number of events in this series: {num_indices}. Testing {test_number}.')
        se_indices = se_indices[:test_number]
    with h5py.File(cut_output_file_path, 'w') as cut_out:
        uid_group = cut_out.create_group('UID')
        series_group = uid_group.create_group(f'S{series_number}')
        # Find how long it takes on average to get cut data for a single event and file
        all_times = []
        for cut_file in os.listdir(cut_data_csv_folder):
            start_time = time.time()
            if '.csv' not in cut_file:
                continue
            if 'small' in cut_file:
                continue
            if 'ID' in cut_file:
                continue
            # Load cut_data_file
            cut_file_path = os.path.join(cut_data_csv_folder, cut_file)
            cut_data = pd.read_csv(cut_file_path, header=None, names=['bool value'])
            cut_data = cut_data.astype(bool)
            file_time = time.time()
            if is_test:
                print(f'Loading file took {file_time - start_time:.2f} seconds')
            data_name = cut_file[:-4] # cut off .csv for naming
            for index in se_indices:
                try:
                    event_number = cdms_ids.loc[cdms_ids['index'] == index, 'event_number'].values[0]
                except:
                    if is_test:
                        print(f'No event number found.')
                    event_number = False
                    continue
                if f'E{event_number}' not in series_group:
                    event_group = series_group.create_group(f'E{event_number}')
                else:
                    event_group = series_group[f'E{event_number}']
                try:
                    value_at_event = get_event_cut_data(index, cut_data)
                except:
                    value_at_event = ''
                try:
                    event_group.create_dataset(data_name, data=value_at_event)
                except Exception as e:
                    print(f'Error saving {data_name} for {event_number}:\n{e}')
            end_time = time.time()
            seconds_per_cut = end_time - file_time
            all_times.append(seconds_per_cut)
            if is_test:
                print(f'{data_name} took {seconds_per_cut:.2f} seconds.\n')
        average_seconds_per_cut = sum(all_times) / len(all_times)
        if is_test:
            print(f'On average, each event takes {average_seconds_per_cut/test_number:.2f} seconds per cut.')
            minutes_for_full_series = (num_indices * (average_seconds_per_cut/test_number))/60
            print(f'To get the cut data for every event in this series would take around {minutes_for_full_series:.2f} minutes, or around {minutes_for_full_series/60:.2f} hours.')

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
    selected_event_dictionary = {}
    for _, row in selected_rows.iterrows():
        series_number = row['series_number']
        event_number = row['event_number']
        if series_number not in selected_event_dictionary:
            selected_event_dictionary[series_number] = [event_number]
        else:
            selected_event_dictionary[series_number].append(event_number)

    return selected_event_dictionary

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

    return series_and_true_events, series_and_false_events

def fetch_events_from_dict(cdms_ids, selected_event_dictionary, parsed_hdf5_file_path, cut_data_csv_folder, trace_output_folder, cut_output_folder):
    """
    Use dictionary generated by find_overlapping_bool to fetch cut and 
    trace data for every event found.
    """
    for series, events in selected_event_dictionary.items():
        for event in events:
            trace_out_filename = f'intersect_S{series}_E{event}_trace_out.hdf5'
            trace_output_file_path = os.path.join(trace_output_folder, trace_out_filename)

            cut_out_filename = f'intersect_S{series}_E{event}_cut_out.hdf5'
            cut_output_file_path = os.path.join(cut_output_folder, cut_out_filename)
            get_single_event_metadata(cdms_ids, event, parsed_hdf5_file_path, cut_data_csv_folder, trace_output_file_path, cut_output_file_path)