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

hdf5_file_path = "/data3/afisher/test/parsed_file.hdf5"

event_number, series_number = get_series_numbers(hdf5_file_path)
print(f'Series number: {series_number}')
print(f'Events in series: {len(event_number)}')


# Given a series number, find the number of events in the series
def get_event_info(series_number):
    directory = '/data3/afisher/cdmslite-run3-cuts-output/'
    # Load cdms id file
    id_path = directory+'ID_CDMSliteR3.csv'

    # Load id file into a dataframe
    cdms_ids = pd.read_csv(id_path, header = None, names = ['index', 'series-event'])
    # Split series-event column into 'series_number' and 'event_number'
    cdms_ids[['series_number', 'event_number']] = cdms_ids['series-event'].str.split('-', expand = True)
    cdms_ids = cdms_ids.drop('series-event', axis=1)

    events = []
    for _, row in cdms_ids.iterrows():
        if row['series_number'] == series_number:
            events.append(row['event_number'])
    

#event_len = get_event_info(series_number)
event_len = get_event_info(11502121819)
print(event_len)