#include <iostream>
#include <fstream>
#include <string>

#include "kaitai/kaitaistruct.h"

#include "awkward/Slice.h"
#include "awkward/builder/ArrayBuilder.h"
#include "awkward/builder/ArrayBuilderOptions.h"

using namespace std;
namespace ak = awkward;

// Data type: scdms
ak::ArrayBuilder _read(kaitai::kstream* ks) {

	// initialize array for scdms seq
	ak::ArrayBuilder scdmss(ak::ArrayBuilderOptions(1024, 2.0));

	while(!ks->is_eof()) {
		scdmss.beginrecord();
		// Read commands for sequence: scdms_header
		// currently on n_triggers
		kaitai::kstruct* n_triggers = ks->read_switch (scdms_hdr.format_version)();

		// Read commands for sequence: trailer
		// Read commands for sequence: v_two_trig_meta
		// Read commands for sequence: primitive
		// currently on packed
		uint32_t packed = ks->read_u4le();

		// Read commands for sequence: detector
	}
	// currently on packed
	uint32_t packed = ks->read_u4le();

	// currently on n_pre_pulse_samples
	uint32_t n_pre_pulse_samples = ks->read_u4le();

	// currently on n_on_pulse_samples
	uint32_t n_on_pulse_samples = ks->read_u4le();

	// currently on n_post_pulse_samples
	uint32_t n_post_pulse_samples = ks->read_u4le();

	// currently on sample_rate_low
	uint16_t sample_rate_low = ks->read_u2le();

	// currently on sample_rate_high
	uint16_t sample_rate_high = ks->read_u2le();

	// currently on sample
	uint16_t sample = ks->read_u2le();

}
// currently on packed_1
uint32_t packed_1 = ks->read_u4le();

// currently on trigger_id
uint32_t trigger_id = ks->read_u4le();

// currently on trigger_type
trigger_types_t trigger_type = ks->read_u4le→TriggerTypes();

// currently on global_timestamp_low
uint32_t global_timestamp_low = ks->read_u4le();

// currently on global_timestamp_high
uint32_t global_timestamp_high = ks->read_u4le();

// currently on packed_2
uint32_t packed_2 = ks->read_u4le();

// currently on length_of_entry
uint32_t length_of_entry = ks->read_u4le();

}
// Read commands for sequence: det_meta
// Read commands for sequence: channel
}
// currently on packed
uint32_t packed = ks->read_u4le();

}
// currently on packed_1
uint32_t packed_1 = ks->read_u4le();

// currently on trigger_id
uint32_t trigger_id = ks->read_u4le();

// currently on event_number
uint32_t event_number = ks->read_u4le();

// currently on packed_2
uint32_t packed_2 = ks->read_u4le();

// currently on global_timestamp_low
uint32_t global_timestamp_low = ks->read_u4le();

// currently on global_timestamp_high
uint32_t global_timestamp_high = ks->read_u4le();

// currently on packed_3
uint32_t packed_3 = ks->read_u4le();

// currently on length_of_entry
uint32_t length_of_entry = ks->read_u4le();

}
// currently on packed
uint32_t packed = ks->read_u4le();

}
// currently on packed_1
uint32_t packed_1 = ks->read_u4le();

// currently on ut
uint32_t ut = ks->read_u4le();

// currently on packed_2
uint32_t packed_2 = ks->read_u4le();

// currently on rt_run_time
uint16_t rt_run_time = ks->read_u2le();

// currently on trig_time
uint16_t trig_time = ks->read_u2le();

// currently on packed_3
uint32_t packed_3 = ks->read_u4le();

// currently on peak_amplitude
uint16_t peak_amplitude = ks->read_u2le();

// currently on trig_word
uint16_t trig_word = ks->read_u2le();

}
// Read commands for sequence: v_one_trig_meta
// Read commands for sequence: primitive
// currently on packed
uint32_t packed = ks->read_u4le();

// Read commands for sequence: detector
}
// currently on packed_1
uint32_t packed_1 = ks->read_u4le();

// currently on dcrc0_version
uint8_t dcrc0_version = ks->read_u1();

// currently on dcrc0_serial_num
uint8_t dcrc0_serial_num = ks->read_u1();

// currently on dcrc1_version
uint8_t dcrc1_version = ks->read_u1();

// currently on dcrc1_serial_num
uint8_t dcrc1_serial_num = ks->read_u1();

// currently on packed_2
uint32_t packed_2 = ks->read_u4le();

// currently on packed_3
uint32_t packed_3 = ks->read_u4le();

// currently on packed_4
uint32_t packed_4 = ks->read_u4le();

}
}
}
