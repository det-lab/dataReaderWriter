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
		List(animal)s.beginrecord();
		// Read commands for sequence: animal_entry

		List(animal)s.beginrecord();
		uint8_t str_len = ks->read_u1();
		List(animal)s.field_check("str_len");
		List(animal)s.integer(str_len);

		std::string species = kaitai::kstream::bytes_to_str(, std::string("UTF-8"))
		List(animal)s.field_check("species");
		List(animal)s.string(species);

		uint8_t age = ks->read_u1();
		List(animal)s.field_check("age");
		List(animal)s.integer(age);

		uint16_t weight = ks->read_u2le();
		List(animal)s.field_check("weight");
		List(animal)s.integer(weight);

		List(animal)s.endrecord();
	}
	List(animal)s.endrecord();
}
}
