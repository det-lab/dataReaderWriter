import pandas as pd
import h5py

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
            header_group = f['logical_rcrds/admin_rcrd']
            header_groups = [key for key in header_group.keys() if key.startswith('admin_rcrd')]
            num_header_groups = len(header_groups)

            # Find the requested event number in the file
            for i in range(num_header_groups):
                admin_group = header_groups[i]
                event_num_path = f'logical_rcrds/admin_rcrd/{admin_group}/event_number_in_series'
                if event_num_path in f:
                    event_data = f[event_num_path]
                    event_num = int(event_data[()])
                    if event_number == event_num:
                        print(f"Event found at location {i}")
                        logical_rcrd_array = f['logical_rcrds/logical_rcrd_data']
                        relevant_array = logical_rcrd_array[i]
                        trace_data = relevant_array[6]
                        print(f'Trace len: {len(trace_data)}')


#hdf5_file_path = "/data3/afisher/test/parsed_file.hdf5"
hdf5_file_path = '/home/afisher@novateur.com/dataReaderWriter/scdms_soudan/parsed.hdf5'

event_number, series_number = get_series_numbers(hdf5_file_path)
print(f'Series number: {series_number}')
print(f'Events in series: {len(event_number)}')
print(f'Event range: {event_number[-1]-event_number[0]} from {event_number[0]} to {event_number[-1]}')

get_event_data(hdf5_file_path, event_number[1])