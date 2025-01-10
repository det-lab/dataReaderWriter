print('Running file')
import sys
sys.path.append('/home/afisher@novateur.com/dataReaderWriter/scdms_soudan/construct-examples/')
sys.path.append('/home/afisher@novateur.com/dataReaderWriter/scdms_soudan/construct-examples/parsing/')
import csv_metadata
#import soudan_parser
print('Imports successful')
import os

# 
src_directory = '/data3/afisher/soudan-R135/01150212_1819'
parsed_directory = '/data3/afisher/test/parsed_files'
trace_output_directory = '/data3/afisher/test/parsed_files/trace_outputs'
cut_output_directory = '/data3/afisher/test/parsed_files/cut_outputs'
cdms_ids_file_path = '/data3/afisher/cdmslite-run3-cuts-output/ID_CDMSliteR3.csv'
os.makedirs(trace_output_directory, exist_ok=True)
os.makedirs(cut_output_directory, exist_ok=True)

# First, parse the files in src_directory and send the parsed files to parsed_directory
def parse_directory(src_directory, parsed_directory, trace_output_directory, cut_output_directory):
    for file in os.listdir(src_directory):
        # Avoid entering folders
        if 'outputs' in file:
            continue
        print(f'Parsing {file}...')
        input_file_path = f'{src_directory}/{file}'
        output_parsed_file_path = f'{parsed_directory}/{file}_parsed.hdf5'
        if os.path.exists(output_parsed_file_path):
            print(f'\nSkipping {file}, {output_parsed_file_path} already exists.')
            continue
        try:
            soudan_parser.parse_file(input_file_path, output_parsed_file_path, use_test_parse=False)
            print(f'\n{file} successfully parsed.')
        except Exception as e:
            print(f'Error parsing file:\n{e}')

def parse_series_folder(cdms_ids, parsed_directory, cut_data_csv_folder, trace_output_file_path, cut_output_file_path):
    for parsed_file in os.listdir(parsed_directory):
        if not os.path.isfile(os.path.join(parsed_directory, parsed_file)):
            continue
        csv_metadata.get_series_full_metadata(cdms_ids, parsed_directory, cut_data_csv_folder, trace_output_file_path, cut_output_file_path)

cdms_ids = csv_metadata.load_id_file(cdms_ids_file_path)

cut_data_csv_folder = '/data3/afisher/cdmslite-run3-cuts-output/'
trace_output_file_path = '/home/afisher@novateur.com/dataReaderWriter/NovateurData/full_series_trace_test.hdf5'
cut_output_file_path = '/home/afisher@novateur.com/dataReaderWriter/NovateurData/full_series_cut_test.hdf5'
parse_series_folder(cdms_ids, parsed_directory, cut_data_csv_folder, trace_output_file_path, cut_output_file_path)