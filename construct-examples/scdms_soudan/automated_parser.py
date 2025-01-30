print('Running file')
import sys
sys.path.append('/home/afisher@novateur.com/dataReaderWriter/scdms_soudan/construct-examples/')
import csv_metadata
import os
import time # Count how long it takes to run
print('Imports successful')

src_directory = '/data3/afisher/soudan-R135/01150212_1819'
parsed_file_folder = '/data3/afisher/test/parsed_files'
trace_output_directory = '/data3/afisher/test/parsed_files/trace_outputs'
cut_output_directory = '/data3/afisher/test/parsed_files/cut_outputs'
cdms_ids_file_path = '/data3/afisher/cdmslite-run3-cuts-output/ID_CDMSliteR3.csv'
os.makedirs(trace_output_directory, exist_ok=True)
os.makedirs(cut_output_directory, exist_ok=True)

# First, parse the files in src_directory and send the parsed files to parsed_directory
def parse_directory(src_directory, parsed_file_folder, trace_output_directory, cut_output_directory):
    for file in os.listdir(src_directory):
        # Avoid entering folders
        if 'outputs' in file:
            continue
        print(f'Parsing {file}...')
        input_file_path = f'{src_directory}/{file}'
        output_parsed_file_path = f'{parsed_file_folder}/{file}_parsed.hdf5'
        if os.path.exists(output_parsed_file_path):
            print(f'\nSkipping {file}, {output_parsed_file_path} already exists.')
            continue
        try:
            soudan_parser.parse_file(input_file_path, output_parsed_file_path, use_test_parse=False)
            print(f'\n{file} successfully parsed.')
        except Exception as e:
            print(f'Error parsing file:\n{e}')

def parse_series_folder(cdms_ids, parsed_file_folder, parsed_hdf5_file_path, cut_data_csv_folder, trace_output_file_path, cut_output_file_path):
    # Attempt to create series cut file
    cut_start_time = time.time()
    print(f'Getting series cut data...')
    try:
        csv_metadata.get_series_cut_data(cdms_ids, parsed_hdf5_file_path, cut_data_csv_folder, cut_output_file_path, is_test=False)
        cut_end_time = time.time()
        print(f'Attempt sucessful after {(cut_end_time - cut_start_time)/60:.2f} minutes')
    except Exception as e:
        cut_end_time = time.time()
        print(f'Error generating series trace metadata file:\n{e}')
        print(f'Attempt took {(cut_end_time - cut_start_time)/60:.2f} minutes')
    
    trace_start_time = time.time()
    print(f"Getting series trace data...")
    try:
        csv_metadata.get_series_trace_data(parsed_file_folder, trace_output_file_path, is_test=False)
        trace_end_time = time.time
        print(f"Attempt successful after {(trace_end_time - trace_start_time)/60:.2f} minutes.")
    except Exception as e:
        trace_end_time = time.time()
        print(f"Error generating series trace metadata file:\n{e}")
        print(f'Attempt took {(trace_end_time - trace_start_time)/60:.2f} minutes.')

print('Loading cdms_ids file.')
cdms_ids = csv_metadata.load_id_file(cdms_ids_file_path)
print('File loaded.')

cut_data_csv_folder = '/data3/afisher/cdmslite-run3-cuts-output/'
trace_output_file_path = '/data3/afisher/test/parsed_files/trace_outputs/full_series_trace_test.hdf5'
cut_output_file_path = '/data3/afisher/test/parsed_files/cut_outputs/full_series_cut_test.hdf5'
parsed_hdf5_file_path = '/data3/afisher/test/parsed_files/01150212_1819_F0001_parsed.hdf5'

parse_series_folder(cdms_ids, parsed_file_folder, parsed_hdf5_file_path, cut_data_csv_folder, trace_output_file_path, cut_output_file_path)