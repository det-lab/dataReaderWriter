print('Running file')
import sys
sys.path.append('/home/afisher@novateur.com/dataReaderWriter/scdms_soudan/')
sys.path.append('/home/afisher@novateur.com/dataReaderWriter/scdms_soudan/parsing/')
import csv_metadata
import metadata
print('Metadata successfully imported')
import soudan_parser
print('soudan_parser successfully imported')
import os

# 
src_directory = '/data3/afisher/soudan-R135/01150212_1819'
parsed_directory = '/data3/afisher/test/parsed_files'
trace_output_directory = '/data3/afisher/test/parsed_files/trace_outputs'
cut_output_directory = '/data3/afisher/test/parsed_files/cut_outputs'
cdms_ids_file_path = '/data3/afisher/cdmslite-run3-cuts-output/ID_CDMSliteR3.csv'
os.makedirs(trace_output_directory, exist_ok=True)
os.makedirs(cut_output_directory, exist_ok=True)

# First, parse the files in directory and send the parsed files to parsed_directory
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
        try:
            print('Creating cut and trace outputs for the first event in the file...')
            trace_output_path = f'{trace_output_directory}/{file}_trace_output.hdf5'
            cut_output_path = f'{cut_output_directory}/{file}_cut_output.hdf5'
            series_number, event_numbers = metadata.get_series_and_event_numbers(output_parsed_file_path)
            event_number = event_numbers[0]
            csv_metadata.get_csv_metadata(event_number, cdms_ids_file_path, output_parsed_file_path, trace_output_path, cut_output_path, is_test=False)
            print('Trace and cut output files created.')
        except Exception as e:
            print(f'Error creating cut or trace output:\n{e}')

    except Exception as e:
        print(f'Error parsing file:\n{e}')