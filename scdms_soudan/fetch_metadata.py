import pandas as pd
import h5py
import matplotlib.pyplot as plt
import numpy as np
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

    return event_numbers, series_number

def get_event_data(hdf5_file_path, event_number):

    with h5py.File(hdf5_file_path, 'r') as f:
        admin_group = f['logical_rcrds/admin_rcrd']
        admin_groups = [key for key in admin_group.keys() if key.startswith('admin_rcrd')]
        admin_groups = sorted(admin_groups, key=lambda x: int(re.search(r'\d+', x).group()))
        num_admin_groups = len(admin_groups)
        print(f'Num admins: {num_admin_groups}')

        trace_group = f['logical_rcrds/trace_data']
        trace_groups = [key for key in trace_group.keys() if key.startswith('trace_data')]
        trace_groups = sorted(trace_groups, key=lambda x: int(re.search(r'\d+', x).group()))
        num_trace_groups = len(trace_groups)
        print(f'Num trace: {num_trace_groups}')

        buffer_group = f['logical_rcrds/soudan_buffer']
        buffer_groups = [key for key in buffer_group.keys() if key.startswith('soudan_history_buffer')]
        buffer_groups = sorted(buffer_groups, key=lambda x: int(re.search(r'\d+', x).group()))
        num_buffer_groups = len(buffer_groups)
        print(f'Num buffers: {num_buffer_groups}')

        charge_hdr_group = f['hdrs/charge_config']
        charge_hdr_groups = [key for key in charge_hdr_group.keys() if key.startswith('charge_config_')]
        charge_hdr_groups = sorted(charge_hdr_groups, key=lambda x: int(re.search(r'\d+', x).group()))
        num_charge_groups = len(charge_hdr_groups)
        print(f'Num charge groups: {num_charge_groups}')

        phonon_hdr_group = f['hdrs/phonon_config']
        phonon_hdr_groups = [key for key in phonon_hdr_group.keys() if key.startswith('phonon_config_')]
        phonon_hdr_groups = sorted(phonon_hdr_groups, key=lambda x: int(re.search(r'\d+', x).group()))
        num_phonon_groups = len(phonon_hdr_groups)
        print(f'Num phonon groups: {num_phonon_groups}')

        # Find the requested event number in the file
        for i in range(num_admin_groups):
            admin_group = admin_groups[i]
            event_num_path = f'logical_rcrds/admin_rcrd/{admin_group}/event_number_in_series'

            buffer_group = buffer_groups[i]
            charge_hdr_group = charge_hdr_groups[i]
            phonon_hdr_group = phonon_hdr_groups[i]
            trace_group = trace_groups[i]

            num_trig_times_path = f'logical_rcrds/soudan_buffer/{buffer_group}/num_trigger_times'
            charge_det_code_path = f'hdrs/charge_config/{charge_hdr_group}/detector_code'
            phonon_det_code_path = f'hdrs/phonon_config/{phonon_hdr_group}/detector_code'
            trace_det_code_path = f'logical_rcrds/trace_data/{trace_group}/detector_code'
            
            if event_num_path in f:
                event_data = f[event_num_path]
                event_num = int(event_data[()])

                if event_number == event_num:
                    print(f"Event {event_number} found at location {i}")
                    print(f'Admin group: {admin_group}')
                    print(f'Buffer group: {buffer_group}')

                    print(f'Charge hdr group: {charge_hdr_group}')
                    charge_det_code = f[charge_det_code_path]
                    charge_det_code = int(charge_det_code[()])
                    print(f'Charge det code: {charge_det_code}')

                    print(f'Phonon hdr group: {phonon_hdr_group}')
                    phonon_det_code = f[phonon_det_code_path]
                    phonon_det_code = int(phonon_det_code[()])
                    print(f'Phonon det code: {phonon_det_code}')

                    trace_path_base = f'logical_rcrds/trace_data/{trace_group}'
                    trace_type = None

                    trigger_times = f[num_trig_times_path]
                    trigger_times = int(trigger_times[()])
                    print(f'trigger times: {trigger_times}')
                    
                    trace_det_code = f[trace_det_code_path]
                    det_code = int(trace_det_code[()])
                    print(f'Detector code: {det_code}')

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
#print(f'Series number: {series_number}')
#print(f'Events in series: {max(event_numbers) - min(event_numbers)}')
#print(f'Event range from {min(event_numbers)} to {max(event_numbers)}')

trace, type = get_event_data(hdf5_file_path, event_numbers[1])
print(type)
x = np.arange(len(trace))
plt.scatter(x, trace)
plt.show()