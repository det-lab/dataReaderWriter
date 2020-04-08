#include <iostream>
#include <fstream>
#include <string>

#include "kaitai/kaitaistruct.h"

#include "awkward/Slice.h"
#include "awkward/builder/ArrayBuilder.h"
#include "awkward/builder/ArrayBuilderOptions.h"

using namespace std;
namespace ak = awkward;

// Data type: midas
ak::ArrayBuilder _read(kaitai::kstream* ks) {

	// initialize array for midas seq
	ak::ArrayBuilder midass(ak::ArrayBuilderOptions(1024, 2.0));

	while(!ks->is_eof()) {
		midass.beginrecord();
		// Read commands for sequence: event
		// Read commands for sequence: bank_hdr
		// currently on bank
		kaitai::kstruct* bank = ks->read_switch ((bank_header.flags &amp; (1 &lt;&lt; 4)))();

	}
	// Read commands for sequence: event_hdr
	// currently on data_block
	kaitai::kstruct* data_block = ks->read_switch (event_header.event_id)();

}
// currently on odb
std::string odb = ks->read_();

}
// currently on name
std::string name = ks->read_str(UTF-8)();

// currently on type
uint16_t type = ks->read_u2le();

// currently on size
uint16_t size = ks->read_u2le();

// Read commands for sequence: scdms
}
// currently on all_bank_size
uint32_t all_bank_size = ks->read_u4le();

// currently on flags
uint32_t flags = ks->read_u4le();

}
// currently on event_id
uint16_t event_id = ks->read_u2le();

// currently on trigger_mask
uint16_t trigger_mask = ks->read_u2le();

// currently on serial_number
uint32_t serial_number = ks->read_u4le();

// currently on time_stamp
uint32_t time_stamp = ks->read_u4le();

// currently on evt_data_size
uint32_t evt_data_size = ks->read_u4le();

}
// currently on name
std::string name = ks->read_str(UTF-8)();

// currently on type
uint32_t type = ks->read_u4le();

// currently on size
uint32_t size = ks->read_u4le();

// Read commands for sequence: scdms
}
}
}
