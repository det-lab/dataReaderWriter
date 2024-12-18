import h5py
import matplotlib.pyplot as plt
import numpy as np
import re
import sys
sys.path.append('/home/afisher@novateur.com/dataReaderWriter/scdms_soudan/parsing/')
import soudan_parser
print('Imports successful')

def get_series_num(parsed_hdf5_file_path):
    with h5py.File(parsed_hdf5_file_path, 'r') as f:
        series_pattern = r'S(\d+)'
        for group_name in f:
            series_match = re.match(series_pattern, group_name)
            if series_match:
                series_number = series_match.group(1)
    return series_number

# Given an hdf5 file, return the event numbers in the file
def get_series_and_event_numbers(parsed_hdf5_file_path):
    event_numbers = []
    with h5py.File(parsed_hdf5_file_path, 'r') as f:
        event_pattern = r'E(\d+)'
        series_number = get_series_num(parsed_hdf5_file_path)
        series_group = f[f'S{series_number}']
        for group_name in series_group:
            event_match = re.match(event_pattern, group_name)
            if event_match:
                event_number = event_match.group(1)
                event_numbers.append(event_number)
    return series_number, event_numbers

def print_structure(name, obj):
    if isinstance(obj, h5py.Group):
        print(f'Group: {name}')
    elif isinstance(obj, h5py.Dataset):
        print(f"Dataset: {name}, Shape: {obj.shape}, Data type: {obj.dtype}")
        # Print the dataset values (for small datasets)
        data = obj[()]
        print(f"Values: {data}")

def get_event_data(parsed_hdf5_file, event_number, metadata_file,  trace_output_file_path, cut_output_file_path):
    """
    Given an event number and a parsed hdf5 file,
    generate a new file with trace data from every detector
    and a file with the cut data for the event.
    """
    series_number = get_series_num(parsed_hdf5_file)
    with h5py.File(parsed_hdf5_file, 'r') as parsed_f:
        series_group = parsed_f[f'S{series_number}']
        event_group = series_group[f'E{event_number}']
        detector_groups = [key for key in event_group.keys() if key.startswith('det_code_')]
        base_path = f'S{series_number}/E{event_number}'
        charge_traces = []
        phonon_traces = []
        veto_traces = []
        error_traces = []

        charge_detector_set = set()
        phonon_detector_set = set()
        veto_detector_set = set()
        error_detector_set = set()

        with h5py.File(trace_output_file_path, 'w') as output_f:
            series_group = output_f.create_group(f'S{series_number}')
            event_group = series_group.create_group(f'E{event_number}')
            for detector_group in detector_groups:
                # Grab detector code
                detector_pattern = r'det_code_(\d+)'
                detector_match = re.match(detector_pattern, detector_group)
                detector_code = detector_match.group(1)

                # Copy data from parsed hdf5 file to output
                new_det_group = event_group.create_group(detector_group)

                trace_type_path = f'{base_path}/{detector_group}/trace_type'     
                trace_type = parsed_f[trace_type_path][()]
                trace_type = trace_type.decode('utf-8')

                trace_path = f'{base_path}/{detector_group}/trace'
                trace = parsed_f[trace_path][()]

                det_type_path = f'{base_path}/{detector_group}/detector_type'
                det_type = parsed_f[det_type_path][()]
                det_type = det_type.decode('utf-8')

                new_det_group.create_dataset('trace_type', data=trace_type)
                new_det_group.create_dataset('trace', data=trace)
                new_det_group.create_dataset('detector_type', data=det_type)

                if trace_type == 'Charge':
                    charge_traces.append(trace)
                    charge_detector_set.add(detector_code)
                elif trace_type =='Phonon':
                    phonon_traces.append(trace)
                    phonon_detector_set.add(detector_code)
                elif trace_type =='Veto':
                    veto_traces.append(trace)
                    veto_detector_set.add(detector_code)
                elif trace_type =='Error':
                    error_traces.append(trace)
                    error_detector_set.add(detector_code)
            detector_info_group = output_f.create_group('detector_lists')
            detector_info_group.create_dataset('charge_detectors', data=list(charge_detector_set))
            detector_info_group.create_dataset('phonon_detectors', data=list(phonon_detector_set))
            detector_info_group.create_dataset('veto_detectors', data=list(veto_detector_set))
            detector_info_group.create_dataset('error_detectors', data=list(error_detector_set))
    
    with h5py.File(metadata_file, 'r') as meta_f:
        event_path = f'UID/series/{series_number}/{event_number}'
        if event_path not in meta_f:
            print(f'Error: Path {event_path} not found in metadata file.')
            print(f'Available paths:', list(meta_f['UID/series'].keys()))
            return
        meta_event_group = meta_f[event_path]
        cut_groups = [key for key in meta_event_group.keys()]

        with h5py.File(cut_output_file_path, 'w') as cut_f:
            output_cut_group = cut_f.create_group('cut_data')
            for group in cut_groups:
                group_data_path = f'{event_path}/{group}'
                group_data = meta_f[group_data_path]
                group_data = group_data[()]
                output_cut_group.create_dataset(group, data=group_data)

    try:
        for trace in charge_traces:
            x = np.arange(len(trace))
            plt.scatter(x, trace, s=1)
        plt.title(f'Charge traces for event {event_number}')
        plt.show()

        for trace in phonon_traces:
            x = np.arange(len(trace))
            plt.scatter(x, trace, s=1)
        plt.title(f'Phonon traces for event {event_number}')
        plt.show()

        for trace in veto_traces:
            x = np.arange(len(trace))
            plt.scatter(x, trace, s=1)
        plt.title(f'Veto traces for event {event_number}')
        plt.show()

        for trace in error_traces:
            if len(trace) == 4096:
                x = np.arange(len(trace))
                plt.scatter(x, trace, s=1)
        plt.title(f'Phonon error traces for event {event_number}')
        plt.show()

        for trace in error_traces:
            if len(trace) == 2048:
                x = np.arange(2048)
                plt.scatter(x, trace, s=1)
        plt.title(f'Charge error traces for event {event_number}')
        plt.show()
    except Exception as e:
        print(f'Error plotting data:\n{e}')

def collect_series_data(parsed_hdf5_file, metadata_file, trace_output_file_path, cut_output_file_path):
    """
    Collect all trace and cut data from a parsed hdf5 file,
    generating one file with all of the trace data and another
    with all of the cut data.
    """
    series_number, event_numbers = get_series_and_event_numbers(parsed_hdf5_file)
    event_group_paths = []
    # Use parsed file to generate trace file
    with h5py.File(parsed_hdf5_file, 'r') as parsed_f:
        print('Accessing parsed file...')
        series_group = parsed_f[f'S{series_number}']
        event_groups = [key for key in series_group.keys() if key.startswith('E')]

        charge_detector_set = set()
        phonon_detector_set = set()
        veto_detector_set = set()
        error_detector_set = set()

        with h5py.File(trace_output_file_path, 'w') as trace_f:
            print('Writing new trace file...')
            out_series_group = trace_f.create_group(f'S{series_number}')
            for event_group in event_groups:
                # Save paths for later access
                event_group_path = f'S{series_number}/{event_group}'
                event_group_f = parsed_f[event_group_path]
                event_group_paths.append(event_group_path)
                trace_out_event_group = out_series_group.create_group(f'{event_group}')

                detector_groups = [key for key in event_group_f.keys() if key.startswith('det_code_')]
                for detector_group in detector_groups:
                    # Grab detector code
                    detector_pattern = r'det_code_(\d+)'
                    detector_match = re.match(detector_pattern, detector_group)
                    detector_code = detector_match.group(1)

                    # Copy data from parsed hdf5 file to output
                    new_det_group = trace_out_event_group.create_group(detector_group)

                    trace_path = f'{event_group_path}/{detector_group}/trace'
                    trace = parsed_f[trace_path][()]

                    trace_type_path = f'{event_group_path}/{detector_group}/trace_type'
                    trace_type = parsed_f[trace_type_path][()]
                    trace_type = trace_type.decode('utf-8')

                    det_type_path = f'{event_group_path}/{detector_group}/detector_type'
                    det_type = parsed_f[det_type_path][()]
                    det_type = det_type.decode('utf-8')

                    new_det_group.create_dataset('trace_type', data=trace_type)
                    new_det_group.create_dataset('trace', data=trace)
                    new_det_group.create_dataset('detector_type', data=det_type)

                    if trace_type == 'Charge':
                        charge_detector_set.add(detector_code)
                    elif trace_type =='Phonon':
                        phonon_detector_set.add(detector_code)
                    elif trace_type =='Veto':
                        veto_detector_set.add(detector_code)
                    elif trace_type =='Error':
                        error_detector_set.add(detector_code)

            detector_info_group = trace_f.create_group('detector_lists')
            detector_info_group.create_dataset('charge_detectors', data=list(charge_detector_set))
            detector_info_group.create_dataset('phonon_detectors', data=list(phonon_detector_set))
            detector_info_group.create_dataset('veto_detectors', data=list(veto_detector_set))
            detector_info_group.create_dataset('error_detectors', data=list(error_detector_set))
        print('Finished creating trace file.')

    # Use metadata file to collect cut info
    meta_event_groups = []
    # Dictionary to hold cut info for each event
    event_cut_dictionary = {}
    with h5py.File(metadata_file, 'r') as meta_f:
        print(f'Accessing metadata file...')
        series_path = f'UID/series/{series_number}'
        if series_path not in meta_f:
            print(f'Error: Path {series_path} not found in metadata file.')
            pass
        for event_number in event_numbers:
            event_path = f'UID/series/{series_number}/{event_number}'
            if event_path not in meta_f:
                #print(f'Error: No cut information found for event {event_number} ')
                pass
            else:
                #print(f'Cut information found for event {event_number}')
                meta_out_event_group = meta_f[event_path]
                meta_event_groups.append(meta_out_event_group)
                cut_groups = [key for key in meta_out_event_group.keys()]
                # Put event group and cut data into a shared dictionary to be pulled from
                if meta_out_event_group not in event_cut_dictionary:
                    event_cut_dictionary[meta_out_event_group] = cut_groups
        #print(event_cut_dictionary)
        with h5py.File(cut_output_file_path, 'w') as cut_f:
            print('Writing output cut file...')
            output_cut_group = cut_f.create_group('cut_data')
            for meta_out_group, cut_group in event_cut_dictionary.items():
                #print(meta_out_group, cut_group)
                # Select event number for events that have cut information
                event_number_pattern = r'\/UID\/series\/\d+\/(\d+)'
                group_name = meta_out_group.name
                event_number_match = re.match(event_number_pattern, group_name)
                # f to avoid confusion
                event_number_f = event_number_match.group(1)
                event_number_group_out = output_cut_group.create_group(event_number_f)
                for group in cut_group:
                    group_data_path = f'{group_name}/{group}'
                    group_data = meta_f[group_data_path]
                    group_data = group_data[()]
                    event_number_group_out.create_dataset(group, data=group_data)

print('Running...')
#metadata_file = '/data3/afisher/soudan_output/metadata.hdf5'
metadata_file = '/home/afisher@novateur.com/dataReaderWriter/NovateurData/metadata_small.hdf5'
parsed_hdf5_file = '/data3/afisher/test/parsed_files/01150212_1819_F0001_parsed.hdf5'
trace_output_file = '/home/afisher@novateur.com/dataReaderWriter/NovateurData/get_trace_data_test.hdf5'
cut_output_file = '/home/afisher@novateur.com/dataReaderWriter/NovateurData/get_cut_data_test.hdf5'

series_number, event_numbers = get_series_and_event_numbers(parsed_hdf5_file)
event_number = event_numbers[0]
print(f'Series number: {series_number}')
print(f'Testing on event_number: {event_number}')
print(f'Number of events: {len(event_numbers)}')
get_event_data(parsed_hdf5_file, event_number, metadata_file, trace_output_file, cut_output_file)

# Testing collect_series_data
trace_output_collect_test = '/home/afisher@novateur.com/dataReaderWriter/NovateurData/collect_series_trace_test.hdf5'
cut_output_collect_test = '/home/afisher@novateur.com/dataReaderWriter/NovateurData/collect_series_cut_test.hdf5'
collect_series_data(parsed_hdf5_file, metadata_file, trace_output_collect_test, cut_output_collect_test)