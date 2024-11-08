import h5py
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import re

directory = '/data3/afisher/cdmslite-run3-cuts-output/'
# Load cdms id file
id_path = directory+'ID_CDMSliteR3.csv'
# Create array of file names in directory
file_names = []

# Load id file into a dataframe
cdms_ids = pd.read_csv(id_path, header = None, names = ['index', 'series-event'])
# Split series-event column into 'series_number' and 'event_number'
cdms_ids[['series_number', 'event_number']] = cdms_ids['series-event'].str.split('-', expand = True)
cdms_ids = cdms_ids.drop('series-event', axis=1)

for file in os.listdir(directory):
    if os.path.isfile(os.path.join(directory, file)):
        file_names.append(file)

def create_tables(output_path):
    # Create a dataframe with the ID indices
    bool_df = pd.DataFrame(cdms_ids['index'])
    with h5py.File(output_path, 'w') as f:
        short_names = []

        # pattern fits files like: cut_output_bg-restricted_IsGlitch_chisq_CDMSliteR3.csv
        pattern = r'(?:(cut_output_bg-|out_bg-))(?:restricted_)(.*?)(?:_CDMSliteR3.csv)'

        # allCuts_pattern fits files like: out_bg-restricted_allCutsOld_inclPmult.csv
        allCuts_pattern = r'(?:.*?-restricted_)(.*?)(?:\.csv)'

        for file in file_names:
            if file in ['ID_CDMSliteR3.csv', 'README.md']:
                continue
            # Skip test files
            if "_small" in file:
                continue
            match = re.search(pattern, file)
            allCuts_match = re.search(allCuts_pattern, file)
            # Fill list with names to create easy to read group names
            if match:
                name = match.group(1) + match.group(2)

            elif allCuts_match:
                name = allCuts_match.group(1)
            
            if name:
                short_names.append(name)

                # Load data into df
                cut_data_df = pd.read_csv(os.path.join(directory+file), header = None, names = [name])
                # Convert df into boolean - turns 1's and 0's into True and False
                cut_data_df[name] = cut_data_df[name].astype(bool)
                # Add the boolean column to the main DataFrame
                bool_df[name] = cut_data_df[name]

        cut_data_group = f.create_group("cut_data")

        # Save each boolean column as a separate dataset
        for col in bool_df.columns[1:]:
            #print(f"Saving column {col} with type {bool_df[col].dtype}")
            cut_data_group.create_dataset(col, data=bool_df[col].to_numpy())

        id_group = f.create_group('UID')

        id_group.create_dataset('index', data=cdms_ids.iloc[:,0].to_numpy())
        id_group.create_dataset('series_ids', data=cdms_ids.iloc[:,1].to_numpy())
        id_group.create_dataset('event_numbers', data=cdms_ids['event_number'].to_numpy())

    #return bool_df

# Given an index, return
def relate_index(index, bool_df):
    # Load ID data into function
    directory = '/data3/afisher/cdmslite-run3-cuts-output/'
    id_path = directory+'ID_CDMSliteR3.csv'
    cdms_ids = pd.read_csv(id_path, header = None, names = ['index', 'series-event'])

    # Split series-event column into 'series_number' and 'event_number'
    cdms_ids[['series_number', 'event_number']] = cdms_ids['series-event'].str.split('-', expand = True)
    cdms_ids = cdms_ids.drop('series-event', axis=1)

    series = cdms_ids.loc[index, 'series_number']
    event_number = cdms_ids.loc[index, 'event_number']
    cut_info = bool_df.loc[index]
    
    return series, event_number, cut_info

# Given an event number, return index


def relate_event(event_number):
    # Load ID data into function
    directory = '/data3/afisher/cdmslite-run3-cuts-output/'
    id_path = directory+'ID_CDMSliteR3.csv'
    cdms_ids = pd.read_csv(id_path, header = None, names = ['index', 'series-event'])
    
    # Split series-event column into 'series_number' and 'event_number'
    cdms_ids[['series_number', 'event_number']] = cdms_ids['series-event'].str.split('-', expand = True)
    cdms_ids = cdms_ids.drop('series-event', axis=1)

    row = cdms_ids[cdms_ids['event_number'] == event_number]

    if not row.empty:
        index = row['index'].values[0]
    else:
        print(f'Event number {event_number} not found.')
        index = None
    
    return index

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

def get_event_data(hdf5_file_path, output_file_path, event_number):

    with h5py.File(hdf5_file_path, 'r') as f:
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

            with h5py.File(output_file_path, 'w') as new_f:
                trace_match_list_group = new_f.create_group('trace_match')
                trace_match_list_group.create_dataset('trace_list', data=trace_match_list)
                trace_match_list_group.create_dataset('data_type', data=type)

def fetch_data(event_number, bool_df, hdf5_file_path):
    # Use event number to find cut data
    index = relate_event(event_number, bool_df)
    series, event_number, cut_info = relate_index(index, bool_df)

    # Use event number to find matching data
    trace_match_list, trace_type = get_event_data(hdf5_file_path, event_number)

    # Plot data
    x = np.arange(len(trace_match_list[0]))
    for trace in trace_match_list:
        plt.scatter(x, trace)
    plt.title(trace_type)
    plt.show()

    print(cut_info)

    return cut_info


output_path = '/home/afisher@novateur.com/dataReaderWriter/scdms_soudan/metadata.hdf5'
#create_tables(output_path)
bool_df = create_tables(output_path)
#series, event_number, cut_info = relate_index(30, bool_df)

hdf5_file_path = "/data3/afisher/test/parsed_file.hdf5"

# fetch_data test
event_numbers, series_number = get_series_numbers(hdf5_file_path)
print(f'Series number: {series_number}')
event_number = event_numbers[0]
print(f'Event number: {event_number}')
index = relate_event(event_number, bool_df)
print(f'Index: {index}')
cut_info = fetch_data(event_number, bool_df, hdf5_file_path)


#print(bool_df.head())