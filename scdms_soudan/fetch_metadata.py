import h5py
import re

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
    # Sort event numbers
    event_numbers = sorted(event_numbers)

    return event_numbers, series_number

def get_event_data(hdf5_file_path, event_number):

    with h5py.File(hdf5_file_path, 'r') as f:
        # Load admin_rcrds to find event_number
        admin_group = f['logical_rcrds/admin_rcrd']
        admin_groups = [key for key in admin_group.keys() if key.startswith('admin_rcrd')]
        admin_groups = sorted(admin_groups, key=lambda x: int(re.search(r'\d+', x).group()))
        num_admin_groups = len(admin_groups)

        # Load trace_data to relate event_number to data
        trace_group = f['logical_rcrds/trace_data']
        trace_groups = [key for key in trace_group.keys() if key.startswith('trace_data')]
        trace_groups = sorted(trace_groups, key=lambda x: int(re.search(r'\d+', x).group()))
        num_trace_groups = len(trace_groups)

        # Ratio between trace groups and admin groups
        step_size = num_trace_groups/num_admin_groups
        #print(f'Step size: {step_size}')

        # Find the requested event number in the file
        for i in range(num_admin_groups):
            # Iterate through admin groups to find a match
            admin_group = admin_groups[i]
            event_num_path = f'logical_rcrds/admin_rcrd/{admin_group}/event_number_in_series'
            event_num = f[event_num_path]
            event_num = int(event_num[()])

            # Find match - extract data
            if event_number == event_num:
                #print(f"Event {event_number} found at location {i}")
                #print(f'Admin group: {admin_group}')

                # Find corresponding trace_data
                trace_group = trace_groups[i]
                #print(f'Trace group: {trace_group}')

                trace_det_code_path = f'logical_rcrds/trace_data/{trace_group}/detector_code'
                trace_det_code = f[trace_det_code_path]
                trace_det_code = int(trace_det_code[()])
                #print(f'Trace detector code: {trace_det_code}')

                # Collect traces with matching detector codes
                trace_match_list = []
                trace_path_base = f'logical_rcrds/trace_data/'
                # Allow for missing data
                type = None
                for trace in trace_groups:
                    # Find all traces with matching detector codes
                    match_det_code_path = f'logical_rcrds/trace_data/{trace}/detector_code'
                    match_det_code = f[match_det_code_path]
                    match_det_code = int(match_det_code[()])
                    #print(f'Trace det code: {trace_det_code}')
                    type_path_base = f'{trace_path_base}{trace}/'

                    # Find if trace is charge, phonon, veto, or error
                    if match_det_code == trace_det_code:
                        charge_match_path = f'{type_path_base}charge_trace'
                        phonon_match_path = f'{type_path_base}phonon_trace'
                        veto_match_path = f'{type_path_base}veto_trace'
                        error_match_path = f'{type_path_base}error_trace'

                        if charge_match_path in f:
                            trace_data = f[charge_match_path][()]
                            trace_match_list.append(trace_data)
                            type = 'charge_trace'
                        elif phonon_match_path in f:
                            trace_data = f[phonon_match_path][()]
                            trace_match_list.append(trace_data)
                            type = 'phonon_trace'
                        elif veto_match_path in f:
                            trace_data = f[veto_match_path][()]
                            trace_match_list.append(trace_data)
                            type = 'veto_trace'
                        elif error_match_path in f:
                            trace_data = f[error_match_path][()]
                            trace_match_list.append(trace_data)
                            type = 'error_trace'
                        else:
                            print(f'No valid trace found for {event_number}.')
                            trace_data = None
                            type = None

                return trace_match_list, type

hdf5_file_path = "/data3/afisher/test/parsed_file.hdf5"
#hdf5_file_path = '/home/afisher@novateur.com/dataReaderWriter/scdms_soudan/parsed.hdf5'

event_numbers, series_number = get_series_numbers(hdf5_file_path)
print(f'Series number: {series_number}')
print(f'Events in series: {max(event_numbers) - min(event_numbers) + 1}')
print(f'Events range from {min(event_numbers)} to {max(event_numbers)}')
print()

traces, type = get_event_data(hdf5_file_path, event_numbers[0])