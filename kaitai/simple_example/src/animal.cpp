// This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

#include <memory>
#include "animal.h"



animal_t::animal_t(kaitai::kstream* p__io, kaitai::kstruct* p__parent, animal_t* p__root) : kaitai::kstruct(p__io) {
    m__parent = p__parent;
    m__root = this;
    m_entry = 0;
    _read();
}

void animal_t::_read() {
    m_entry = new std::vector<animal_entry_t*>();
    {
        int i = 0;
        while (!m__io->is_eof()) {
            m_entry->push_back(new animal_entry_t(m__io, this, m__root));
            i++;
        }
    }
}

animal_t::~animal_t() {
    for (std::vector<animal_entry_t*>::iterator it = m_entry->begin(); it != m_entry->end(); ++it) {
        delete *it;
    }
    delete m_entry;
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
