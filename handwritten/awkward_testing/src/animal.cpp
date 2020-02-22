// This is an edited kaitai-generated file modified to store data in an awkward array


#include <memory>
#include "animal.h"

namespace ak = awkward;

animal_t::animal_t(kaitai::kstream* p__io, kaitai::kstruct* p__parent, animal_t* p__root) : kaitai::kstruct(p__io), m_entry(ak::FillableOptions(1024, 2.0)) {
    m__parent = p__parent;
    m__root = this;
    //m_entry = 0;
    _read();
}

void animal_t::_read() {
    //ak::FillableArray m_entry(ak::FillableOptions(1024, 2.0));
    {
        int i = 0;
        while (!m__io->is_eof()) {
            animal_entry_t this_animal = animal_entry_t(m__io, this, m__root);
           
            // start record for i-th animal
            m_entry.beginrecord();

            // record species name
            m_entry.field_check("Name");
            m_entry.string(this_animal.species());

            // record age
            m_entry.field_check("Age");
            m_entry.integer(this_animal.age());
        
            // record weight
            m_entry.field_check("Weight");
            m_entry.integer(this_animal.weight());
        
            // end record for i-th animal
            m_entry.endrecord();

            i++;
        }
    }
}

animal_t::~animal_t() {
}

animal_t::animal_entry_t::animal_entry_t(kaitai::kstream* p__io, animal_t* p__parent, animal_t* p__root) : kaitai::kstruct(p__io) {
    m__parent = p__parent;
    m__root = p__root;
    _read();
}

void animal_t::animal_entry_t::_read() {
    m_str_len = m__io->read_u1();
    m_species = kaitai::kstream::bytes_to_str(m__io->read_bytes(str_len()), std::string("UTF-8"));
    m_age = m__io->read_u1();
    m_weight = m__io->read_u2le();
}

animal_t::animal_entry_t::~animal_entry_t() {
}
