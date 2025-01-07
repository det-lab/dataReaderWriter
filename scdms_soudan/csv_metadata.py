import h5py
import pandas as pd
import os
import re
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
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

# Use original .csv files instead of constructed hdf5 file
def get_single_event_metadata(event_number, cdms_ids_file_path, parsed_hdf5_file, trace_output_file_path, cut_output_file_path, is_test=True):
    """
    Create two hdf5 files containing the cut data information and trace data information
    from a given parsed data file.
    """
    print('Loading CDMS ID file...')
    if is_test:
        #Only use the first 10 lines for testing
        cdms_ids = pd.read_csv(cdms_ids_file_path, header=None, names = ['index', 'series-event']).head(10)
    else:
        cdms_ids = pd.read_csv(cdms_ids_file_path, header = None, names = ['index', 'series-event'])
    
    # split series-event column into 'series_number' and 'event_number'
    cdms_ids[['series_number', 'event_number']] = cdms_ids['series-event'].str.split('-', expand = True)
    # drop redundant column
    cdms_ids = cdms_ids.drop('series-event', axis=1)
    
    print('File loaded.')
    series_number = get_series_num(parsed_hdf5_file)
    # Find the index of the given event
    se_index = cdms_ids.loc[(cdms_ids['series_number'] == series_number) & (cdms_ids['event_number'] == event_number)].index
    se_index = se_index[0]
    print(f'Series number: {series_number}')
    print(f'Series/Event index: {se_index}')
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
    
    print('Trace output file created.')

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

def find_valid_series_events(cut_data_file_path, cdms_ids_file_path, is_test=True):
    """
    Given a .csv cut data file, return two dictionaries,
    one of True series-event pairs and another of False series-event pairs
    """
    print('Loading CDMS ID file...')
    if is_test:
        #Only use the first 10 lines for testing
        cdms_ids = pd.read_csv(cdms_ids_file_path, header=None, names = ['index', 'series-event']).head(10)
    else:
        cdms_ids = pd.read_csv(cdms_ids_file_path, header = None, names = ['index', 'series-event'])
    
    # split series-event column into 'series_number' and 'event_number'
    cdms_ids[['series_number', 'event_number']] = cdms_ids['series-event'].str.split('-', expand = True)
    # drop redundant column
    cdms_ids = cdms_ids.drop('series-event', axis=1)
    
    print('File loaded.')

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
#cut_data_file = '/data3/afisher/cdmslite-run3-cuts-output/out_bg-restricted_IsSquarePulse_CDMSliteR3.csv'
#valid, invalid = find_valid_series_events(cut_data_file, cdms_ids_file_path, is_test=False)
#
#series_number, event_numbers = get_series_and_event_numbers(parsed_hdf5_file_path)
#event_number = event_numbers[3]
#print(f'Range of event numbers in file: {event_numbers[0]} to {event_numbers[-1]}')
#get_csv_metadata(event_number, cdms_ids_file_path, parsed_hdf5_file_path, trace_output_file_path, cut_output_file_path, is_test=False)