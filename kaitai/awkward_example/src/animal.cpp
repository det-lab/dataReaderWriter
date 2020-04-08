#include <iostream>
#include <fstream>
#include <string>

#include "kaitai/kaitaistruct.h"

#include "awkward/Slice.h"
#include "awkward/builder/ArrayBuilder.h"
#include "awkward/builder/ArrayBuilderOptions.h"

using namespace std;
namespace ak = awkward;

// Data type: animal
ak::ArrayBuilder _read(kaitai::kstream* ks) {

	// initialize array for animal seq
	ak::ArrayBuilder animals(ak::ArrayBuilderOptions(1024, 2.0));

	while(!ks->is_eof()) {
		animals.beginrecord();
		// Read commands for sequence: animal_entry

		animals.beginrecord();
		uint8_t str_len = ks->read_u1();
		animals.field_check("str_len");
		animals.integer(str_len);

		std::string species = ks->read_str(UTF-8)();
		animals.field_check("species");
		animals.string(species);

		uint8_t age = ks->read_u1();
		animals.field_check("age");
		animals.integer(age);

		uint16_t weight = ks->read_u2le();
		animals.field_check("weight");
		animals.integer(weight);

		animals.endrecord();
	}
	animals.endrecord();
}
}
