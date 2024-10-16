import h5py
import pandas as pd
from collections import Counter
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

# Load some cut files for testing
allCuts_old = 'out_bg-restricted_allCutsOld_inclPmult.csv'
isGlitch = 'cut_output_bg-restricted_IsGlitch_chisq_CDMSliteR3.csv'
badGPSTime = 'out_bg-restricted_BadGPStime_CDMSliteR3.csv'

allCuts_old_df = pd.read_csv(directory+allCuts_old, header = None, names=['allCuts_old'])
isGlitch_df = pd.read_csv(directory+isGlitch, header = None, names=['IsGlitch_chisq'])
badGPSTime_df = pd.read_csv(directory+badGPSTime, header = None, names=['BadGPSTime'])

# Convert 0's and 1's to False and True
allCuts_old_df['allCuts_old'] = allCuts_old_df['allCuts_old'].astype(bool)
isGlitch_df['IsGlitch_chisq'] = isGlitch_df['IsGlitch_chisq'].astype(bool)
badGPSTime_df['BadGPSTime'] = badGPSTime_df['BadGPSTime'].astype(bool)

combined_df = pd.concat([cdms_ids['index'], allCuts_old_df, isGlitch_df, badGPSTime_df], axis=1)

#print(combined_df.head())

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

        #
        for file in file_names:
            if file in ['ID_CDMSliteR3.csv', 'README.md']:
                continue
            match = re.search(pattern, file)
            allCuts_match = re.search(allCuts_pattern, file)
            # Fill list with names to create easy to read group names
            if match:
                name = match.group(1) + match.group(2)

            elif allCuts_match:
                name = allCuts_match.group(1)
            
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

    #return bool_df

output_path = 'metadata.hdf5'
create_tables(output_path)
#bool_df = create_tables(output_path)

#print(bool_df.head())