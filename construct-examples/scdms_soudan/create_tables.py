import h5py
import pandas as pd
import os
import re
import sys
from collections import defaultdict
sys.path.append('/home/afisher@novateur.com/dataReaderWriter/scdms_soudan/')
import metadata

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

# Do the same for the small version for testing
cdms_ids_small_path = '/data3/afisher/cdmslite-run3-cuts-output/ID_CDMSliteR3_small.csv'
cdms_ids_small = pd.read_csv(cdms_ids_small_path, header=None, names = ['index', 'series-event'])
cdms_ids_small[['series_number', 'event_number']] = cdms_ids_small['series-event'].str.split('-', expand=True)
cdms_ids_small = cdms_ids_small.drop('series-event', axis=1)

#for file in os.listdir(directory):
#    if os.path.isfile(os.path.join(directory, file)):
#        file_names.append(file)

def create_tables(output_file):
    # Create a dataframe with the ID indices
    bool_df = pd.DataFrame(cdms_ids['index'])
    with h5py.File(output_file, 'w') as f:
        # Shorten file names for readability
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

        id_group = f.create_group('UID')
        series_group = id_group.create_group('series')
        unique_series = cdms_ids['series_number'].unique()
        for series in unique_series:
            # Create a group for each series number
            uid_series_group = series_group.create_group(f'{series}')

            # Filter events in the series
            series_events = cdms_ids[cdms_ids['series_number'] == series]

            # Load the cut_data for each event
            for _, row in series_events.iterrows():
                event_number = row['event_number']
                event_index = row.name
                event_group = uid_series_group.create_group(event_number)

                for col in bool_df.columns[1:]:
                    cut_value = bool_df.loc[event_index, col]
                    event_group.create_dataset(col, data=cut_value)

def create_small_tables(output_path):
    # Create a dataframe with the ID indices
    bool_df = pd.DataFrame(cdms_ids['index'])
    with h5py.File(output_path, 'w') as f:
        short_names = []

        # pattern fits files like: cut_output_bg-restricted_IsGlitch_chisq_CDMSliteR3.csv
        pattern = r'(?:.*?-restricted_)(.*?)(?:\_small.csv)'

        for file in file_names:
            if file in ['ID_CDMSliteR3_small.csv', 'README.md']:
                continue
            match = re.search(pattern, file)
            # Fill list with names to create easy to read group names
            #print(match, file)
            if match:
                name = match.group(1)
                
                #print(match)
                short_names.append(name)

                # Load data into df
                cut_data_df = pd.read_csv(os.path.join(directory+file), header = None, names = [name])
                # Convert df into boolean - turns 1's and 0's into True and False
                cut_data_df[name] = cut_data_df[name].astype(bool)
                # Add the boolean column to the main DataFrame
                bool_df[name] = cut_data_df[name]

        id_group = f.create_group('UID')
        series_group = id_group.create_group('series')
        unique_series = cdms_ids['series_number'].unique()
        for series in unique_series:
            # Create a group for each series number
            uid_series_group = series_group.create_group(f'{series}')

            # Filter events in the series
            series_events = cdms_ids[cdms_ids['series_number'] == series]

            # Load the cut_data as a dataset for each event
            for _, row in series_events.iterrows():
                event_number = row['event_number']
                event_index = row.name
                event_group = uid_series_group.create_group(event_number)

                for col in bool_df.columns[1:]:
                    cut_value = bool_df.loc[event_index, col]
                    event_group.create_dataset(col, data=cut_value)
                  
def create_series_tables(output_folder):
    # Create a dataframe with the ID indices
    bool_df = pd.DataFrame(cdms_ids['index'])
    # Shorten file names for readability
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
    
    unique_series = cdms_ids['series_number'].unique()
    for series in unique_series:
        output_path = f'{output_folder}/S{series}_metadata.hdf5'
        with h5py.File(output_path, 'w') as out_f:
            id_group = out_f.create_group('UID')
            series_group = id_group.create_group(series)
            # Filter events in the series
            series_events = cdms_ids[cdms_ids['series_number'] == series]

            # Load cut_data for each event
            for _, row in series_events.iterrows():
                event_number = row['event_number']
                event_index = row.name
                event_group = series_group.create_group(event_number)

                for col in bool_df.columns[1:]:
                    cut_value = bool_df.loc[event_index, col]
                    event_group.create_dataset(col, data=cut_value)

#create_tables('/data3/afisher/soudan_output/metadata.hdf5')