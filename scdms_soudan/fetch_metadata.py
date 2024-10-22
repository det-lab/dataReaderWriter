import pandas as pd
import h5py
import matplotlib.pyplot as plt
import numpy as np

# Given an hdf5 file, find the series_number
def get_series_numbers(hdf5_file_path):
    event_numbers = []
    
    with h5py.File(hdf5_file_path, 'r') as f:
        if 'logical_rcrds/admin_rcrd/' in f:
            header_group = f['logical_rcrds/admin_rcrd']
            header_groups = [key for key in header_group.keys() if key.startswith('admin_rcrd')]
            num_header_groups = len(header_groups)
            for i in range(num_header_groups):
                admin_group = header_groups[i]
                event_num_path = f'logical_rcrds/admin_rcrd/{admin_group}/event_number_in_series'
                series_num_1_path = f'logical_rcrds/admin_rcrd/{admin_group}/series_number_1'
                series_num_2_path = f'logical_rcrds/admin_rcrd/{admin_group}/series_number_2'

                if event_num_path in f:
                    event_data = f[event_num_path]
                    event_numbers.append(int(event_data[()]))
                if series_num_1_path in f:
                    series_1_number = f[series_num_1_path]
                    series_1_number = int(series_1_number[()])
                if series_num_2_path in f:
                    series_2_number = f[series_num_2_path]
                    series_2_number = int(series_2_number[()])

            series_number = f'{series_1_number}{series_2_number}'

    return event_numbers, series_number

def get_event_data(hdf5_file_path, event_number):

    with h5py.File(hdf5_file_path, 'r') as f:

        if 'logical_rcrds/admin_rcrd/' in f:
            admin_group = f['logical_rcrds/admin_rcrd']
            admin_groups = [key for key in admin_group.keys() if key.startswith('admin_rcrd')]
            num_admin_groups = len(admin_groups)
            print(f'Num admins: {num_admin_groups}')

            trace_group = f['logical_rcrds/trace_data']
            trace_groups = [key for key in trace_group.keys() if key.startswith('trace_data')]
            num_trace_groups = len(trace_groups)
            print(f'Num trace: {num_trace_groups}')

            # Find the requested event number in the file
            for i in range(num_admin_groups):
                admin_group = admin_groups[i]
                event_num_path = f'logical_rcrds/admin_rcrd/{admin_group}/event_number_in_series'
                if event_num_path in f:
                    event_data = f[event_num_path]
                    event_num = int(event_data[()])
                    if event_number == event_num:
                        print(f"Event found at location {i}")
                        trace_group = trace_groups[i]
                        trace_path_base = f'logical_rcrds/trace_data/{trace_group}'
                        trace_type = None
                        if f'{trace_path_base}/charge_trace' in f:
                            trace_type = 'charge_trace'
                        elif f'{trace_path_base}/phonon_trace' in f:
                            trace_type = 'phonon_trace'
                        elif f'{trace_path_base}/veto_trace' in f:
                            trace_type = 'veto_trace'
                        elif f'{trace_path_base}/error_trace' in f:
                            trace_type = 'error_trace'
                        
                        if trace_type:
                            trace_path = f'{trace_path_base}/{trace_type}'
                            trace_data = f[trace_path][:]
                            return trace_data, trace_type
                        else: 
                            print("No valid trace found for this event")
                            return None

hdf5_file_path = "/data3/afisher/test/parsed_file.hdf5"
#hdf5_file_path = '/home/afisher@novateur.com/dataReaderWriter/scdms_soudan/parsed.hdf5'

event_numbers, series_number = get_series_numbers(hdf5_file_path)
print(f'Series number: {series_number}')
print(f'Events in series: {max(event_numbers) - min(event_numbers)}')
print(f'Event range from {min(event_numbers)} to {max(event_numbers)}')

trace, type = get_event_data(hdf5_file_path, event_numbers[0])
x = np.arange(len(trace))
plt.scatter(x, trace)
plt.show()