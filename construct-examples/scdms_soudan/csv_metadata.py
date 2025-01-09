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
print('Imports successful')

# Load cdms id file
directory = '/data3/afisher/cdmslite-run3-cuts-output/'
cdms_ids_file_path = directory+'ID_CDMSliteR3.csv'

# Create list of file names for use in group creation
file_names = []

for file in os.listdir(directory):
    if os.path.isfile(os.path.join(directory, file)):
        file_names.append(file)

print('File list created')

def load_id_file(cdms_ids_file_path):
    cdms_ids = pd.read_csv(cdms_ids_file_path, header = None, names = ['index', 'series-event'])
    # split series-event column into 'series_number' and 'event_number'
    cdms_ids[['series_number', 'event_number']] = cdms_ids['series-event'].str.split('-', expand = True)
    # drop redundant column
    cdms_ids = cdms_ids.drop('series-event', axis=1)
    return cdms_ids

print('Loading ID file...')
cdms_ids = load_id_file(cdms_ids_file_path)
print(f'ID file loaded.')

def get_series_num(parsed_hdf5_file_path):
    with h5py.File(parsed_hdf5_file_path, 'r') as f:
        series_pattern = r'S(\d+)'
        for group_name in f:
            series_match = re.match(series_pattern, group_name)
            if series_match:
                series_number = series_match.group(1)
    return series_number

def get_series_and_event_numbers(parsed_hdf5_file_path):
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

def get_event_trace_data(parsed_hdf5_file_path, series_number, event_number):
    """"
    Collect trace data for a given series event.
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
    Find bool value for series event in a cut data file.
    """
    se_index = cdms_ids.loc[(cdms_ids['series_number'] == series_number) & (cdms_ids['event_number'] == event_number)].index
    se_index = se_index[0]
    # Load cut_data_file
    cut_data = pd.read_csv(cut_data_file, header=None, names=['bool value'])
    cut_data = cut_data.astype(bool)
    # Match index on cut_data_file
    value_at_event = cut_data.iloc[se_index].item()

    return value_at_event

# Use original .csv files instead of constructed hdf5 file
def get_single_event_metadata(cdms_ids, series_number, event_number, parsed_hdf5_file, trace_output_file_path, cut_output_file_path, is_test=True):
    """
    Create two hdf5 files containing the cut data information and trace data information
    from a given parsed data file.
    """
    # load trace data
    with h5py.File(parsed_hdf5_file, 'r') as parsed_f:
        print('Reading input hdf5 file...')
        series_group = parsed_f[f'S{series_number}']
        event_group = series_group[f'E{event_number}']
        detector_groups = [key for key in event_group.keys() if key.startswith('det_code_')]
        base_path = f'S{series_number}/E{event_number}'
        charge_traces = []
        phonon_traces = []
        veto_traces   = []
        error_traces  = []

        charge_detector_set = set()
        phonon_detector_set = set()
        veto_detector_set   = set()
        error_detector_set  = set()

        detector_type_counts = defaultdict(lambda: defaultdict(int))

        # Write the trace_data to trace_output_file_path
        with h5py.File(trace_output_file_path, 'w') as trace_out_f:
            print('Creating trace output file...')
            uid_group = trace_out_f.create_group('UID')
            series_group = uid_group.create_group(f'S{series_number}')
            event_group = series_group.create_group(f'E{event_number}')
            for detector_group in detector_groups:
                # Grab detector code
                detector_pattern = r'det_code_(\d+)'
                detector_match = re.match(detector_pattern, detector_group)
                detector_code = detector_match.group(1)

                # Copy data from parsed hdf5 file to output
                new_det_group = event_group.create_group(detector_group)

                trace_type_path = f'{base_path}/{detector_group}/trace_type'     
                trace_type = parsed_f[trace_type_path][()]
                trace_type = trace_type.decode('utf-8')

                trace_path = f'{base_path}/{detector_group}/trace'
                trace = parsed_f[trace_path][()]

                det_type_path = f'{base_path}/{detector_group}/detector_type'
                det_type = parsed_f[det_type_path][()]
                det_type = det_type.decode('utf-8')

                new_det_group.create_dataset('trace_type', data=trace_type)
                new_det_group.create_dataset('trace', data=trace)
                new_det_group.create_dataset('detector_type', data=det_type)

                if trace_type == 'Charge':
                    charge_traces.append(trace)
                    charge_detector_set.add(detector_code)
                elif trace_type =='Phonon':
                    phonon_traces.append(trace)
                    phonon_detector_set.add(detector_code)
                elif trace_type =='Veto':
                    veto_traces.append(trace)
                    veto_detector_set.add(detector_code)
                elif trace_type =='Error':
                    error_traces.append(trace)
                    error_detector_set.add(detector_code)

                detector_type_counts[det_type][trace_type] += 1
            
            # print how many of each type of channel is in a detector type
            for det_type, trace_counts in detector_type_counts.items():
                charge_count = trace_counts.get('Charge', 0)
                phonon_count = trace_counts.get('Phonon', 0)
                veto_count = trace_counts.get('Veto', 0)
                error_count = trace_counts.get('Error', 0)
                print(f'{det_type} detector type has:\n{charge_count} charge channels,\n{phonon_count} phonon channels,\n{veto_count} veto channels,\nand {error_count} error channels.')
                print()

            detector_info_group = series_group.create_group('detector_lists')
            detector_info_group.create_dataset('charge_detectors', data=list(charge_detector_set))
            detector_info_group.create_dataset('phonon_detectors', data=list(phonon_detector_set))
            detector_info_group.create_dataset('veto_detectors', data=list(veto_detector_set))
            detector_info_group.create_dataset('error_detectors', data=list(error_detector_set))

        print(f'Created trace output file.')

    try:
        for trace in charge_traces:
            x = np.arange(len(trace))
            plt.scatter(x, trace, s=1)
        plt.title(f'Charge traces for event {event_number}')
        plt.show()

        for trace in phonon_traces:
            x = np.arange(len(trace))
            plt.scatter(x, trace, s=1)
        plt.title(f'Phonon traces for event {event_number}')
        plt.show()

        for trace in veto_traces:
            x = np.arange(len(trace))
            plt.scatter(x, trace, s=1)
        plt.title(f'Veto traces for event {event_number}')
        plt.show()

        for trace in error_traces:
            if len(trace) == 4096:
                x = np.arange(len(trace))
                plt.scatter(x, trace, s=1)
        plt.title(f'Phonon error traces for event {event_number}')
        plt.show()

        for trace in error_traces:
            if len(trace) == 2048:
                x = np.arange(2048)
                plt.scatter(x, trace, s=1)
        plt.title(f'Charge error traces for event {event_number}')
        plt.show()
    except Exception as e:
        print(f'Error plotting data:\n{e}')
    
    if is_test:
        #Only use the first 10 lines for testing
        cdms_ids = cdms_ids.head(10)
    series_number = get_series_num(parsed_hdf5_file)
    # Find the index of the given event
    se_index = cdms_ids.loc[(cdms_ids['series_number'] == series_number) & (cdms_ids['event_number'] == event_number)].index
    se_index = se_index[0]
    print(f'Series number: {series_number}')
    print(f'Series/Event index: {se_index}')

    # Use csv files to create an hdf5 cut_file
    with h5py.File(cut_output_file_path, 'w') as cut_f:
        print('Creating cut output file...')
        id_group = cut_f.create_group('UID')
        series_group = id_group.create_group(f'S{series_number}')
        event_group = series_group.create_group(f'E{event_number}')
        for file in file_names:
            # skip these files
            if file in ['ID_CDMSliteR3_small.csv', 'README.md']:
                    continue
            group_name = None
            if is_test:
                try:
                    if '_small' not in file:
                        continue
                    group_name = file[:-4]
                except Exception as e:
                    print(f'Error creating group:\n{e}')
                    return
            
            else:
                try:
                    # skip test files
                    if "_small" in file:
                        continue
                    group_name = file[:-4] # remove .csv from file name

                except Exception as e:
                    print(f'Error creating group:\n{e}')
                    return
            if group_name:
                if is_test:
                    print(f'Group {group_name} created.')
                    
                # if creating group_name succeeds, open file and get value at index
                file_path = os.path.join(directory, file)
                if is_test:
                    print(f'Adding data from: {file_path}')

                cut_data_df = pd.read_csv(file_path, header=None, names=['bool value'])
                # convert to boolean
                cut_data_df = cut_data_df.astype(bool)
                if is_test:
                    print(f'{group_name} head:\n{cut_data_df.head().to_string(index=False)}')

                # store value at series/event index
                value_at_index = cut_data_df.iloc[se_index].item()
                #print(f'Creating group: {group_name}')
                try:
                    cut_group = event_group.create_group(group_name)
                    cut_group.create_dataset(f'bool', data=value_at_index)
                except Exception as e:
                    print(f'Error creating group: {group_name}\n{e}')

                if is_test:
                    print(f'Group: {group_name} Value: {value_at_index}')
        print('Cut output file created.')

#print(f'Testing get_single_event_metadata')
#parsed_hdf5_file = '/data3/afisher/test/parsed_files/01150212_1819_F0001_parsed.hdf5'
#series_number, event_numbers = get_series_and_event_numbers(parsed_hdf5_file)
#event_number = event_numbers[0]
#trace_output_file_path = '/home/afisher@novateur.com/dataReaderWriter/NovateurData/single_event_trace_test.hdf5'
#cut_output_file_path = '/home/afisher@novateur.com/dataReaderWriter/NovateurData/single_event_cut_test.hdf5'
#get_single_event_metadata(cdms_ids, series_number, event_number, parsed_hdf5_file, trace_output_file_path, cut_output_file_path, is_test=False)

def get_series_full_metadata(cdms_ids, parsed_file_folder, cut_data_csv_folder, trace_output_file_path, cut_output_file_path, is_test=True):
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

            parsed_file = os.path.join(parsed_file_folder, parsed_file)

            if parsed_file.endswith('_parsed.hdf5'):
                series_number, event_numbers = get_series_and_event_numbers(parsed_file)
                if not series_group_created:
                    series_group = uid_group.create_group(f"S{series_number}")
                    series_group_created = True
                
                if is_test:
                    event_numbers = event_numbers[:10]
                    print(f'Event numbers: {event_numbers}')

                for event_number in event_numbers:
                    try:
                        event_group = series_group.create_group(f'E{event_number}')
                        det_code_dict = get_event_trace_data(parsed_file, series_number, event_number)
                        
                        for det_code, datasets in det_code_dict.items():
                            det_code_group = event_group.create_group(det_code)
                            for dataset_name, data in datasets.items():
                                det_code_group.create_dataset(dataset_name, data=data)

                    except Exception as e:
                        print(f'Error generating trace output for event {event_number}:\n{e}')
        if is_test:
            print(f'Completed collecting trace data for series: {series_number}.')

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
                    event_numbers = event_numbers[:10]
                for event_number in event_numbers:
                    event_group = series_group.create_group(f'E{event_number}')
                    for cut_file in os.listdir(cut_data_csv_folder):
                        if '_small' in cut_file:
                            continue
                        if '.csv' not in cut_file:
                            continue
                        cut_file_path = os.path.join(cut_data_csv_folder, cut_file)
                        try:
                            value_at_event = get_event_cut_data(cdms_ids, cut_file_path, series_number, event_number)
                            event_group.create_dataset(cut_file, data=value_at_event)
                        except Exception as e:
                            print(f'Error saving {cut_file} for event {event_number}:\n{e}')

        if is_test:
            print(f'Completed collecting cut data for series: {series_number}')

#parsed_hdf5_file_path = '/home/afisher@novateur.com/dataReaderWriter/NovateurData/01150212_1819_F0001_parsed.hdf5'
print(f'Testing get_series_full_metadata...')
parsed_file_folder = '/home/afisher@novateur.com/dataReaderWriter/NovateurData/'
cut_data_csv_folder = '/data3/afisher/cdmslite-run3-cuts-output/'
trace_output_file_path = '/home/afisher@novateur.com/dataReaderWriter/NovateurData/full_series_trace_test.hdf5'
cut_output_file_path = '/home/afisher@novateur.com/dataReaderWriter/NovateurData/full_series_cut_test.hdf5'

#parsed_file_folder = '/data3/afisher/test/parsed_files/'
get_series_full_metadata(cdms_ids, parsed_file_folder, cut_data_csv_folder, trace_output_file_path, cut_output_file_path, is_test=True)

def find_overlapping_bool(cdms_ids, cut_data_csv_folder, true_list, false_list, is_test=True):
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
        
true_list = [
    'out_bg-restricted_Random_CDMSliteR3.csv',                     # 0-49 ALL TRUE 
    'out_bg-restricted_IsSpot_CDMSliteR3.csv',                     # 1, 2, 6, 17, 20, 21, 29, 35, 45, 49 TRUE
    ]

false_list = [
    'out_bg-restricted_IsBadSeries_CDMSliteR3.csv',                # 0-49 ALL FALSE
    'cut_output_bg-restricted_GoodPhononStartTime_CDMSliteR3.csv', # 9, 18, 21, 27, 29, 35, 41, 45 FALSE
    ]

#find_overlapping_bool(cdms_ids, cut_data_csv_folder, true_list, false_list, is_test=False)

def find_valid_series_events(cut_data_file_path, cdms_ids, is_test=True):
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
        
# testing
#parsed_hdf5_file_path = '/data3/afisher/test/parsed_files/01150212_1819_F0001_parsed.hdf5'
#trace_output_file_path = '/home/afisher@novateur.com/dataReaderWriter/NovateurData/get_trace_data_test.hdf5'
#cut_output_file_path = '/home/afisher@novateur.com/dataReaderWriter/NovateurData/get_cut_data_test.hdf5'
#
#cut_data_file = '/data3/afisher/cdmslite-run3-cuts-output/cut_output_bg-restricted_Random_CDMSliteR3.csv'
#cut_data_file = '/data3/afisher/cdmslite-run3-cuts-output/cut_output_bg-restricted_IsGlitch_trig_CDMSliteR3.csv'
#cut_data_file = '/data3/afisher/cdmslite-run3-cuts-output/out_bg-restricted_IsSquarePulse_CDMSliteR3.csv'
#valid, invalid = find_valid_series_events(cut_data_file, cdms_ids_file_path, is_test=True)
#series_number, event_numbers = get_series_and_event_numbers(parsed_hdf5_file_path)
#event_number = event_numbers[3]
#print(f'Range of event numbers in file: {event_numbers[0]} to {event_numbers[-1]}')
#get_csv_metadata(event_number, cdms_ids_file_path, parsed_hdf5_file_path, trace_output_file_path, cut_output_file_path, is_test=False)