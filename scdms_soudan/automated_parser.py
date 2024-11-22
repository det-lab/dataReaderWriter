print('Running file')
import sys
sys.path.append('/home/afisher@novateur.com/dataReaderWriter/scdms_soudan/metadata.py')
import metadata
print('Metadata successfully imported')
import os

# For every run file, generate three hdf5 files
# One: The parsed file
# Two: The Cut Data
# Three: The Trace Data

directory = '/data3/afisher/test'
output_dir = '/data3/afisher/test/test_outputs'
os.makedirs(output_dir, exist_ok=True)
metadata_file = '/data3/afisher/soudan_output/metadata.hdf5'

for file in os.listdir(directory):
    if file == 'test_outputs':
        pass
    else:
        print(f'Accessing {file}')
        parsed_hdf5_file = f'{directory}/{file}'
        event_numbers, series = metadata.get_event_numbers(parsed_hdf5_file)
        event_number = event_numbers[0]
        print(f'Testing event {event_number}')
        trace_output_path = os.path.join(output_dir, f'S{series}_E{event_number}_trace_output.hdf5')
        cut_output_path = os.path.join(output_dir, f'S{series}_E{event_number}_cut_output.hdf5')
        print(f'Output paths:\n{trace_output_path}\n{cut_output_path}')
        if os.path.isdir(trace_output_path):
            print(f'Error: {trace_output_path} is a directory')
            break
        if os.path.isdir(cut_output_path):
            print(f'Error: {cut_output_path} is a directory')
            break
        try:
            metadata.get_event_data(parsed_hdf5_file, metadata_file, event_number, trace_output_path, cut_output_path)
            print(f'HDF5 files successfully created for {file}')
        except Exception as e:
            print(f'An error occurred processing {file}: {e}')