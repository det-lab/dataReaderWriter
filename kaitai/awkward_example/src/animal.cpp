// This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

#include <memory>
#include "animal.h"
namespace ak = awkward;

animal_t::animal_t(kaitai::kstream* p__io, kaitai::kstruct* p__parent, animal_t* p__root) : kaitai::kstruct(p__io), m_entry(ak::ArrayBuilderOptions(1024, 2.0)) {
    m__parent = p__parent;
    m__root = this;

    void animal_t::_read() {
        int i = 0;
        while (!m__io->is_eof()) {
            animal_entry_t this_one = animal_entry_t(m__io, this, m__root);
            m_entry.beginrecord();
            m_entry.field_check("Name");
            m_entry.string(this_one.name());
            m_entry.endrecord();
            i++;
        }
    }
}

animal_t::animal_entry_t::animal_entry_t(kaitai::kstream* p__io, animal_t* p__parent, animal_t* p__root) : kaitai::kstruct(p__io), m_entry(ak::ArrayBuilderOptions(1024, 2.0)) {
    m__parent = p__parent;
    m__root = p__root;

    void animal_t::animal_entry_t::_read() {
        m_str_len = m__io->read_u1();
        m_species = kaitai::kstream::bytes_to_str(m__io->read_bytes(str_len()), std::string("UTF-8"));
        m_age = m__io->read_u1();
        m_weight = m__io->read_u2le();
    }
}
