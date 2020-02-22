#ifndef ANIMAL_H_
#define ANIMAL_H_

// This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

#include "kaitai/kaitaistruct.h"
#include <stdint.h>
#include "awkward/Slice.h"
#include "awkward/fillable/FillableArray.h"
#include "awkward/fillable/FillableOptions.h"
#include <vector>
namespace ak = awkward;

#if KAITAI_STRUCT_VERSION < 9000L
#error "Incompatible Kaitai Struct C++/STL API: version 0.9 or later is required"
#endif

class animal_t : public kaitai::kstruct {

public:
    class animal_entry_t;

    animal_t(kaitai::kstream* p__io, kaitai::kstruct* p__parent = 0, animal_t* p__root = 0);

private:
    void _read();

public:
    ~animal_t();

    class animal_entry_t : public kaitai::kstruct {

    public:

        animal_entry_t(kaitai::kstream* p__io, animal_t* p__parent = 0, animal_t* p__root = 0);

    private:
        void _read();

    public:
        ~animal_entry_t();

    private:
        uint8_t m_str_len;
        std::string m_species;
        uint8_t m_age;
        uint16_t m_weight;
        animal_t* m__root;
        animal_t* m__parent;

    public:
        uint8_t str_len() const { return m_str_len; }
        std::string species() const { return m_species; }
        uint8_t age() const { return m_age; }
        uint16_t weight() const { return m_weight; }
        animal_t* _root() const { return m__root; }
        animal_t* _parent() const { return m__parent; }
    };

private:
    ak::FillableArray m_entry;
    animal_t* m__root;
    kaitai::kstruct* m__parent;

public:
    ak::FillableArray entry() const { return m_entry; }
    animal_t* _root() const { return m__root; }
    kaitai::kstruct* _parent() const { return m__parent; }
};

#endif  // ANIMAL_H_
