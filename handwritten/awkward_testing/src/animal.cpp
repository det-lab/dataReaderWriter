#include <iostream>
#include <fstream>
#include <string>

#include "kaitai/kaitaistruct.h"

#include "awkward/Slice.h"
#include "awkward/builder/ArrayBuilder.h"
#include "awkward/builder/ArrayBuilderOptions.h"

using namespace std;
namespace ak = awkward;

ak::ArrayBuilder _read(kaitai::kstream* ks) {

	// initialize array for animal seq
	ak::ArrayBuilder animals(ak::ArrayBuilderOptions(1024, 2.0));

	while(!ks->is_eof()) {
		animals.beginrecord();
		// animal
		
		currently on entry
		animal_entry_t* entry = ks->read_AnimalEntry();
		
		// animal_entry
		
		currently on str_len
		uint8_t str_len = ks->read_u1();
		
		currently on species
		std::string species = ks->read_str(UTF-8)();
		
		currently on age
		uint8_t age = ks->read_u1();
		
		currently on weight
		uint16_t weight = ks->read_u2le();
		
	}
}
}
