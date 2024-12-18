print('Running file')
import sys
sys.path.append('/home/afisher@novateur.com/dataReaderWriter/scdms_soudan/')
sys.path.append('/home/afisher@novateur.com/dataReaderWriter/scdms_soudan/parsing/')
import metadata
print('Metadata successfully imported')
import soudan_parser
print('soudan_parser successfully imported')
import os

# 
directory = '/data3/afisher/soudan-R135/01150212_1819'
parsed_directory = '/data3/afisher/test/parsed_files'
os.makedirs(parsed_directory, exist_ok=True)

# First, parse the files in directory and send the parsed files to parsed_directory
for file in os.listdir(directory):
    # Avoid accidental recursion
    if file == 'parsed_files':
        pass
    print(f'Parsing {file}...')
    input_file_path = f'{directory}/{file}'
    output_file_path = f'{parsed_directory}/{file}_parsed.hdf5'
    try:
        soudan_parser.parse_file(input_file_path, output_file_path, use_test_parse=False)
        print(f'{file} successfully parsed.')
    except Exception as e:
        print(f'Error parsing file:\n{e}')

trace_output_directory = '/data3/afisher/test/parsed_files/trace_outputs'
cut_output_directory = '/data3/afisher/test/parsed_files/cut_outputs'
metadata_file = '/data3/afisher/soudan_output/metadata.hdf5'

# Create trace and cut information files from parsed files
for file in os.listdir(parsed_directory):
    # Avoid accidental recursion
    if file in ['trace_outputs', 'cut_outputs']:
        pass
    print('Collecting trace and cut data...')
    # Grab the file name without _parsed.hdf5
    file_name = file[:-12] 
    trace_output_path = f'{trace_output_directory}/{file_name}_trace_output.hdf5'
    cut_output_path = f'{cut_output_directory}/{file_name}_cut_output.hdf5'
    try:
        metadata.collect_series_data(file, metadata_file, trace_output_path, cut_output_path)
    except Exception as e:
        print(f'Error processing file:\n{e}')