#include <iostream> // std::cout
#include <fstream>  // std::ifstream
#include <string>   // duh

#include "kaitai/kaitaistruct.h"

#include "awkward/Slice.h"
#include "awkward/builder/ArrayBuilder.h"
#include "awkward/builder/ArrayBuilderOptions.h"

using namespace std;
namespace ak = awkward;

ak::ArrayBuilder _read(kaitai::kstream* ks) {

  //init array
  ak::ArrayBuilder animals(ak::ArrayBuilderOptions(1024, 2.0));

  //read loop 
  while(!ks->is_eof()) {

    // start record for i-th animals
    animals.beginrecord();

    // get length of species name
    uint8_t str_len = ks->read_u1();
    //assert(!rf.eof());

    // get species name
    std::string species = kaitai::kstream::bytes_to_str(ks->read_bytes(str_len), std::string("UTF-8"));
    //ks->read_(&name[0], (int)species_len);
    //assert(!rf.eof());
    animals.field_check("species");
    animals.string(species);
  
    // get age
    uint8_t age = ks->read_u1();
    //assert(!rf.eof());
    animals.field_check("age");
    animals.integer(age);

    // get weight
    uint16_t weight = ks->read_u2le();
    //assert(!rf.eof());
    animals.field_check("weight");
    animals.integer(weight);

    // end record for i-th animals
    animals.endrecord();
  }

  return animals;
}
