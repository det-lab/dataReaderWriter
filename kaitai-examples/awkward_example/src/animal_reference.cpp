#include <iostream> // std::cout
#include <fstream>  // std::ifstream
#include <string>   // duh

#include "kaitai/kaitaistruct.h"

//#include "awkward/Slice.h"
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

//**************************OLD BELOW, PROB WRONG****************************//

// This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

// #include <memory>
// #include "animal.h"
// namespace ak = awkward;

// animal_t::animal_t(kaitai::kstream* p__io, kaitai::kstruct* p__parent, animal_t* p__root) : kaitai::kstruct(p__io), m_entry(ak::ArrayBuilderOptions(1024, 2.0)) {
//     m__parent = p__parent;
//     m__root = this;

//     void animal_t::_read() {
//         int i = 0;
//         while (!m__io->is_eof()) {
//             animal_entry_t this_one = animal_entry_t(m__io, this, m__root);
//             m_entry.beginrecord();
//             m_entry.field_check("Name");
//             m_entry.string(this_one.name());
//             m_entry.endrecord();
//             i++;
//         }
//     }
// }

// animal_t::animal_entry_t::animal_entry_t(kaitai::kstream* p__io, animal_t* p__parent, animal_t* p__root) : kaitai::kstruct(p__io), m_entry(ak::ArrayBuilderOptions(1024, 2.0)) {
//     m__parent = p__parent;
//     m__root = p__root;

//     void animal_t::animal_entry_t::_read() {
//         m_str_len = m__io->read_u1();
//         m_species = kaitai::kstream::bytes_to_str(m__io->read_bytes(str_len()), std::string("UTF-8"));
//         m_age = m__io->read_u1();
//         m_weight = m__io->read_u2le();
//     }
// }
