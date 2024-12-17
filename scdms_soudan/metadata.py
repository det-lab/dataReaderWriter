import h5py
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import re
print('Imports successfull')

def get_series_num(parsed_hdf5_file_path):
    with h5py.File(parsed_hdf5_file_path, 'r') as f:
        series_pattern = r'S(\d+)'
        for group_name in f:
            series_match = re.match(series_pattern, group_name)
            if series_match:
                series_number = series_match.group(1)
    return series_number

# Given an hdf5 file, return the event numbers in the file
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

def print_structure(name, obj):
    if isinstance(obj, h5py.Group):
        print(f'Group: {name}')
    elif isinstance(obj, h5py.Dataset):
        print(f"Dataset: {name}, Shape: {obj.shape}, Data type: {obj.dtype}")
        # Print the dataset values (for small datasets)
        data = obj[()]
        print(f"Values: {data}")

def get_event_data(parsed_hdf5_file, event_number, metadata_file,  output_file_path):
    """
    Given an event number and a parsed hdf5 file,
    generate a new file with trace data from every detector
    and the cut data for the event.
    """
    series_number = get_series_num(parsed_hdf5_file)
    with h5py.File(parsed_hdf5_file, 'r') as parsed_f:
        series_group = parsed_f[f'S{series_number}']
        event_group = series_group[f'E{event_number}']
        detector_groups = [key for key in event_group.keys() if key.startswith('det_code_')]
        base_path = f'S{series_number}/E{event_number}'
        charge_traces = []
        phonon_traces = []
        veto_traces = []
        error_traces = []

        with h5py.File(output_file_path, 'w') as output_f:
            series_group = output_f.create_group(f'S{series_number}')
            event_group = series_group.create_group(f'E{event_number}')
            for detector_group in detector_groups:
                # Copy some information from parsed hdf5 file to output
                new_det_group = event_group.create_group(detector_group)

                trace_type_path = f'{base_path}/{detector_group}/trace_type'     
                trace_type = parsed_f[trace_type_path][()]
                trace_type = trace_type.decode('utf-8')

                trace_path = f'{base_path}/{detector_group}/trace'
                trace = parsed_f[trace_path][()]

                new_det_group.create_dataset('trace_type', data=trace_type)
                new_det_group.create_dataset('trace', data=trace)

                if trace_type == 'Charge':
                    charge_traces.append(trace)
                elif trace_type =='Phonon':
                    phonon_traces.append(trace)
                elif trace_type =='Veto':
                    veto_traces.append(trace)
                elif trace_type =='Error':
                    error_traces.append(trace)
    
    with h5py.File(metadata_file, 'r') as meta_f:
        event_path = f'UID/series/{series_number}/{event_number}'
        meta_event_group = meta_f[event_path]
        cut_groups = [key for key in meta_event_group.keys()]

        with h5py.File(output_file, 'w') as cut_f:
            output_cut_group = cut_f.create_group('cut_data')
            for group in cut_groups:
                group_data_path = f'{event_path}/{group}'
                group_data = meta_f[group_data_path]
                group_data = group_data[()]
                output_cut_group.create_dataset(group, data=group_data)

    for trace in charge_traces:
        x = np.arange(len(trace))
        plt.scatter(x, trace)
    plt.title(f'Charge traces for event {event_number}')
    plt.show()

    for trace in phonon_traces:
        x = np.arange(len(trace))
        plt.scatter(x, trace)
    plt.title(f'Phonon traces for event {event_number}')
    plt.show()

    for trace in veto_traces:
        x = np.arange(len(trace))
        plt.scatter(x, trace)
    plt.title(f'Veto traces for event {event_number}')
    plt.show
    

def collect_event_traces(parsed_hdf5_file, output_trace_file):
    """
    Given a parsed hdf5 file, collect all of the trace data in a new file.
    Similar to get_event_data, except not specific to a single event number.
    Groups data by detector code, tells trace type.
    """
    with h5py.File(parsed_hdf5_file, 'r') as f:
        # Load admin_rcrds to find event_number
        admin_group = f['logical_rcrds/admin_rcrd']
        admin_groups = [key for key in admin_group.keys() if key.startswith('admin_rcrd')]
        # Sort the admin groups
        admin_groups = sorted(admin_groups, key=lambda x: int(re.search(r'\d+', x).group()))
        num_admin_groups = len(admin_groups)

        # Load trace_data to relate event_number to data
        trace_group = f['logical_rcrds/trace_data']
        trace_groups = [key for key in trace_group.keys() if key.startswith('trace_data')]
        # Sort the trace groups
        trace_groups = sorted(trace_groups, key=lambda x: int(re.search(r'\d+', x).group()))
        num_trace_groups = len(trace_groups)

        # Ratio between trace groups and admin groups
        step_size = num_trace_groups/num_admin_groups
        print(f'Num of admin records: {num_admin_groups}')
        print(f'Num of trace data groups: {num_trace_groups}')
        print(f'Trace records per admin: {step_size}')

        event_num_set = set()
        event_num_array = []
        for i in range(num_admin_groups):
            #Iterate through admin records, collecting event numbers
            admin_group = admin_groups[i]
            event_num_path = f'logical_rcrds/admin_rcrd/{admin_group}/event_number_in_series'
            event_num = f[event_num_path]
            event_num = int(event_num[()])

            event_num_set.add(event_num)
            event_num_array.append(event_num)
        
        detector_code_set = set()
        detector_code_array = []
        for i in range(num_trace_groups):
            # Iterate through trace data, collecting set of detector codes
            trace_group = trace_groups[i]
            trace_det_code_path = f'logical_rcrds/trace_data/{trace_group}/detector_code'
            trace_det_code = f[trace_det_code_path]
            trace_det_code = int(trace_det_code[()])

            detector_code_set.add(trace_det_code)
            detector_code_array.append(trace_det_code)

        print(f'Number of detector codes: {len(detector_code_set)}')
        print(f'Number of event numbers: {len(event_num_set)}')
        
        traces_by_detector_code = {code: [] for code in set(detector_code_array)}

        # Iterate over trace_groups, adding traces to the correct group of detector codes
        for trace in trace_groups:
            trace_path_base = f'logical_rcrds/trace_data/{trace}'
            trace_det_code_path = f'{trace_path_base}/detector_code'
            trace_det_code = int(f[trace_det_code_path][()])

            # Find path based on trace type
            if f'{trace_path_base}/charge_trace' in f:
                trace_data = f[f'{trace_path_base}/charge_trace'][()]
                trace_type = 'charge_trace'
            elif f'{trace_path_base}/phonon_trace' in f:
                trace_data = f[f'{trace_path_base}/phonon_trace'][()]
                trace_type = 'phonon_trace'
            elif f'{trace_path_base}/veto_trace' in f:
                trace_data = f[f'{trace_path_base}/veto_trace'][()]
                trace_type = 'veto_trace'
            elif f'{trace_path_base}/error_trace' in f:
                trace_data = f[f'{trace_path_base}/error_trace'][()]
                trace_type = 'error_trace'
            else:
                continue  # Skip if no matching trace type

            # Append trace data to the correct list based on detector code
            traces_by_detector_code[trace_det_code].append({
                'trace_data': trace_data,
                'type': trace_type
            })

        with h5py.File(output_trace_file, 'w') as out_f:
            event_number_group = out_f.create_group('event_numbers')
            event_number_group.create_dataset('event_list', data=event_num_array)

            det_group = out_f.create_group('detector_codes')
            for det_code, traces in traces_by_detector_code.items():
                det_code_group = det_group.create_group(str(det_code))
                for i, trace in enumerate(traces):
                    trace_type = trace['type']
                    dataset_name = f'{trace_type}_{i}'
                    det_code_group.create_dataset(dataset_name, data=trace['trace_data'])

print('Running...')
#metadata_file = '/data3/afisher/soudan_output/metadata.hdf5'
metadata_file = '/home/afisher@novateur.com/dataReaderWriter/NovateurData/metadata_small.hdf5'
parsed_hdf5_file = '/data3/afisher/test/test_parse_01150212_1819_F0001.hdf5'
output_file = '/home/afisher@novateur.com/dataReaderWriter/NovateurData/get_event_data_test.hdf5'

series_number, event_numbers = get_series_and_event_numbers(parsed_hdf5_file)
event_number = event_numbers[0]
print(f'Series number: {series_number}')
print(f'Testing on event_number: {event_number}')
print(f'Number of events: {len(event_numbers)}')
get_event_data(parsed_hdf5_file, event_number, metadata_file, output_file)

#trace_output_path = f'/home/afisher@novateur.com/dataReaderWriter/NovateurData/series_{series}_event_{event_number}_trace_output.hdf5'
#cut_output_path = f'/home/afisher@novateur.com/dataReaderWriter/NovateurData/series_{series}_event_{event_number}_cut_output.hdf5'

#get_event_data(parsed_hdf5_file, metadata_file, event_number, trace_output_path, cut_output_path)