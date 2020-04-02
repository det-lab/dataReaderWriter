#include <iostream> // std::cout
#include <fstream>  // std::ifstream
#include <string>   // duh

#include "kaitai/kaitaistruct.h"

#include "awkward/Slice.h"
#include "awkward/builder/ArrayBuilder.h"
#include "awkward/builder/ArrayBuilderOptions.h"

using namespace std;
namespace ak = awkward;

// Current Sequence: animal
ak::ArrayBuilder read_animal(kaitai::kstream* ks) {

  //init array
  ak::ArrayBuilder animals(ak::ArrayBuilderOptions(1024, 2.0));

  while(!ks->is_eof()) {

    animals.beginrecord();

    uint8_t str_len = ks->read_u1();
    //assert(!rf.eof());

    std::string species = kaitai::kstream::bytes_to_str(ks->read_bytes(str_len), std::string("UTF-8"));
    //assert(!rf.eof());
    animals.field_check("species");
    animals.string(species);
  
    uint8_t age = ks->read_u1();
    //assert(!rf.eof());
    animals.field_check("age");
    animals.integer(age);

    uint16_t weight = ks->read_u2le();
    //assert(!rf.eof());
    animals.field_check("weight");
    animals.integer(weight);

    animals.endrecord();
  }

  return animals;
}

// [[ thinking ahead ]]
// Current sequence: next one? presumably?
// Then init a new array and loop through its types? 
