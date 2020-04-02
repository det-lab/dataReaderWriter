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
		animal_entry_t* entry = ks->read_UserTypeInstream(List(animal_entry),None,List())();
		
		// animal_entry
		
		currently on str_len
		uint8_t str_len = ks->read_Int1Type(false)();
		
		currently on species
		std::string species = ks->read_StrFromBytesType(BytesLimitType(Name(identifier(str_len)),None,false,None,None),UTF-8)();
		
		currently on age
		uint8_t age = ks->read_Int1Type(false)();
		
		currently on weight
		uint16_t weight = ks->read_IntMultiType(false,Width2,Some(LittleEndian))();
		
	}
}
}
