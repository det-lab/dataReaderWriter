import h5py
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import re
print('Imports successfull')
# Given an hdf5 file, return the event numbers in the file
def get_event_numbers(parsed_hdf5_file_path):
    event_numbers = []
    with h5py.File(parsed_hdf5_file_path, 'r') as f:
        header_group = f['logical_rcrds/admin_rcrd']
        header_groups = [key for key in header_group.keys() if key.startswith('admin_rcrd')]
        num_header_groups = len(header_groups)

        # Grab series number
        series_num_1_path = f'logical_rcrds/admin_rcrd/{header_groups[0]}/series_number_1'
        series_num_1 = f[series_num_1_path]
        series_num_1 = int(series_num_1[()])
        series_num_2_path = f'logical_rcrds/admin_rcrd/{header_groups[0]}/series_number_2'
        series_num_2 = f[series_num_2_path]
        series_num_2 = int(series_num_2[()])
        
        series = str(series_num_1)+str(series_num_2)

        for i in range(num_header_groups):
            admin_group = header_groups[i]
            event_num_path = f'logical_rcrds/admin_rcrd/{admin_group}/event_number_in_series'
            event_data = f[event_num_path]
            event_numbers.append(int(event_data[()]))

    # Sort event numbers
    event_numbers = sorted(event_numbers)
    
    return event_numbers, series

def get_event_data(parsed_hdf5_file, metadata_file, event_number, trace_output_path, cut_output_path):
    """
    Given an event number and a parsed hdf5 file,
    generate a new hdf5 file containing the trace data
    which corresponds to the event.
    """
    # Start with grabbing the trace data
    with h5py.File(parsed_hdf5_file, 'r') as parsed_f:
        # Load admin_rcrds to find event_number
        admin_group = parsed_f['logical_rcrds/admin_rcrd']
        admin_groups = [key for key in admin_group.keys() if key.startswith('admin_rcrd')]
        # Sort the admin groups
        admin_groups = sorted(admin_groups, key=lambda x: int(re.search(r'\d+', x).group()))
        num_admin_groups = len(admin_groups)
        print(f'Number of admin groups: {num_admin_groups}')

        # Load trace_data to relate event_number to data
        trace_group = parsed_f['logical_rcrds/trace_data']
        trace_groups = [key for key in trace_group.keys() if key.startswith('trace_data')]
        # Sort the trace groups
        trace_groups = sorted(trace_groups, key=lambda x: int(re.search(r'\d+', x).group()))
        num_trace_groups = len(trace_groups)
        print(f'Num trace groups: {num_trace_groups}')

        # Ratio between trace groups and admin groups
        step_size = num_trace_groups/num_admin_groups
        print(f'Ratio between trace and admin groups: {step_size}')

        # Find the requested event number in the file
        for i in range(num_admin_groups):
            # Iterate through admin groups to find a match
            admin_group = admin_groups[i]
            print(f'Admin Group: {admin_group}')
            event_num_path = f'logical_rcrds/admin_rcrd/{admin_group}/event_number_in_series'
            event_num = parsed_f[event_num_path]
            event_num = int(event_num[()])
            print(f'Event number: {event_num}')

            # Find match - extract data
            if event_number == event_num:
                print(f'Found event number: {event_num}')
                # Find corresponding trace_data
                trace_group = trace_groups[i]
                print(f'Trace group: {trace_group}')

                trace_det_code_path = f'logical_rcrds/trace_data/{trace_group}/detector_code'
                trace_det_code = parsed_f[trace_det_code_path]
                trace_det_code = int(trace_det_code[()])
                print(f'Trace detector code: {trace_det_code}')

                # Collect traces with matching detector codes
                trace_match_list = []
                trace_path_base = f'logical_rcrds/trace_data/'
                # Allow for missing data
                type = None
                for trace in trace_groups:
                    # Find all traces with matching detector codes
                    match_det_code_path = f'logical_rcrds/trace_data/{trace}/detector_code'
                    match_det_code = parsed_f[match_det_code_path]
                    match_det_code = int(match_det_code[()])
                    #print(f'Trace det code: {trace_det_code}')
                    type_path_base = f'{trace_path_base}{trace}'

                    # Find if trace is charge, phonon, veto, or error
                    if match_det_code == trace_det_code:
                        print(f'Match found: {match_det_code}')
                        charge_match_path = f'{type_path_base}/charge_trace'
                        phonon_match_path = f'{type_path_base}/phonon_trace'
                        veto_match_path = f'{type_path_base}/veto_trace'
                        error_match_path = f'{type_path_base}/error_trace'

                        if charge_match_path in parsed_f:
                            trace_data = parsed_f[charge_match_path][()]
                            trace_match_list.append(trace_data)
                            type = 'charge_trace'
                        elif phonon_match_path in parsed_f:
                            trace_data = parsed_f[phonon_match_path][()]
                            trace_match_list.append(trace_data)
                            type = 'phonon_trace'
                        elif veto_match_path in parsed_f:
                            trace_data = parsed_f[veto_match_path][()]
                            trace_match_list.append(trace_data)
                            type = 'veto_trace'
                        elif error_match_path in parsed_f:
                            trace_data = parsed_f[error_match_path][()]
                            trace_match_list.append(trace_data)
                            type = 'error_trace'
                        else:
                            print(f'No valid trace found for {event_number}.')
                            trace_data = None
                            type = None

            x = np.arange(len(trace_match_list[0]))
            for trace in trace_match_list:
                plt.scatter(x, trace)
            plt.title(type)
            plt.show()
            print(f'Trace created successfully')

            with h5py.File(trace_output_path, 'w') as trace_f:
                print('Creating trace file')
                trace_match_list_group = trace_f.create_group(f'{event_number}_trace')
                trace_match_list_group.create_dataset('trace_data', data=trace_match_list)
                trace_match_list_group.create_dataset('data_type', data=str(type))
                trace_match_list_group.create_dataset('detector_code', data=match_det_code)
    
    # Next, collect the cut information
    with h5py.File(metadata_file, 'r') as meta_f:
        # Start by finding the series
        print('Creating Cut Data')
        _, series = get_event_numbers(parsed_hdf5_file)
        event_path = f'UID/series/{series}/{event_number}'
        meta_event_group = meta_f[event_path]
        cut_groups = [key for key in meta_event_group.keys()]

        with h5py.File(cut_output_path, 'w') as cut_f:
            cut_event_group = cut_f.create_group(f'{event_number}')
            for group in cut_groups:
                print(f'Cut: {group}')
                group_data_path = event_path+f'/{group}'
                group_data = meta_f[group_data_path]
                group_data = group_data[()]
                cut_event_group.create_dataset(group, data=group_data)

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
metadata_file = '/data3/afisher/soudan_output/metadata.hdf5'
#metadata_file = '/home/afisher@novateur.com/dataReaderWriter/NovateurData/metadata_test.hdf5'
#create_tables(metadata_file)
parsed_hdf5_file = '/data3/afisher/test/01150211_1500_F0001_parsed.hdf5'

event_numbers, series = get_event_numbers(parsed_hdf5_file)
event_number = event_numbers[0]
print(f'Testing on event_number: {event_number}')
print(f'Range of event numbers: {event_numbers[0]}-{event_numbers[-1]}')

trace_output_path = f'/home/afisher@novateur.com/dataReaderWriter/NovateurData/series_{series}_event_{event_number}_trace_output.hdf5'
cut_output_path = f'/home/afisher@novateur.com/dataReaderWriter/NovateurData/series_{series}_event_{event_number}_cut_output.hdf5'

get_event_data(parsed_hdf5_file, metadata_file, event_number, trace_output_path, cut_output_path)