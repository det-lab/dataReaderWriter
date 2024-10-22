import h5py
import pandas as pd
from collections import Counter
import os
import re

directory = '/data3/afisher/cdmslite-run3-cuts-output/'

# Load cdms id file
id_path = directory+'ID_CDMSliteR3_small.csv'
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

        cut_data_group = f.create_group("cut_data")

        # Save the 'index' as a separate dataset
        cut_data_group.create_dataset('index', data=bool_df['index'].to_numpy())

        # Save each boolean column as a separate dataset
        for col in bool_df.columns[1:]:
            cut_data_group.create_dataset(col, data=bool_df[col].to_numpy())

        id_group = f.create_group('UID')

        id_group.create_dataset('index', data=cdms_ids.iloc[:,0].to_numpy())
        id_group.create_dataset('series_ids', data=cdms_ids.iloc[:,1].to_numpy())

    return bool_df

# Given an index, return series, event, and bool_df
def relate_index(index, bool_df):
    # Load ID data into function
    directory = '/data3/afisher/cdmslite-run3-cuts-output/'
    id_path = directory+'ID_CDMSliteR3_small.csv'
    cdms_ids = pd.read_csv(id_path, header = None, names = ['index', 'series-event'])

    # Split series-event column into 'series_number' and 'event_number'
    cdms_ids[['series_number', 'event_number']] = cdms_ids['series-event'].str.split('-', expand = True)
    cdms_ids = cdms_ids.drop('series-event', axis=1)

    series = cdms_ids.loc[index, 'series_number']
    event_number = cdms_ids.loc[index, 'event_number']
    cut_info = bool_df.loc[index]

    return series, event_number, cut_info

# Given an event number, return index
def relate_event(event_number, bool_df):
    # Load ID data into function
    directory = '/data3/afisher/cdmslite-run3-cuts-output/'
    id_path = directory+'ID_CDMSliteR3_small.csv'
    cdms_ids = pd.read_csv(id_path, header = None, names = ['index', 'series-event'])
    
    # Split series-event column into 'series_number' and 'event_number'
    cdms_ids[['series_number', 'event_number']] = cdms_ids['series-event'].str.split('-', expand = True)
    cdms_ids = cdms_ids.drop('series-event', axis=1)

    row = cdms_ids[cdms_ids['event_number'] == event_number]

    if not row.empty:
        index = row['index'].values[0]
    
    return index


output_path = '/home/afisher@novateur.com/dataReaderWriter/scdms_soudan/metadata_small.hdf5'
#create_tables(output_path)
bool_df = create_tables(output_path)
series, event_number, cut_info = relate_index(4, bool_df)
print(f'cut_info:\n{cut_info},\nseries: {series},\nevent_number:{event_number}')
index = relate_event(event_number, bool_df)
print(index)

#print(bool_df.head())