// BSD 3-Clause License; see https://github.com/jpivarski/awkward-1.0/blob/master/LICENSE

#include <iostream> // std::cout
#include <fstream>  // std::ifstream
#include <string>   // duh
#include <assert.h> // for fancy erroring

#include "awkward/Slice.h"
#include "awkward/builder/ArrayBuilder.h"
#include "awkward/builder/ArrayBuilderOptions.h"

using namespace std;
namespace ak = awkward;

ak::ArrayBuilder main(int, char**){

  /* Open the input file in binary mode */
  ifstream infile("data/animal_raw", ifstream::binary);

  /* Create a kaitai stream of the source file */
  kaitai::kstream ks(&infile);


  /* */
  ak::ArrayBuilder zoo = kaitai::something(&ks);

  /* Create an object from the kaitai stream, this object class is what was
     generated from using the kaitai-struct-compiler on the animal.ksy file */
  animal_t zoo = animal_t(&ks);

  /* Get a pointer to the vector containing all the animals */
  ak::FillableArray animal_vec = zoo.entry();
  //vector<animal_t::animal_entry_t*> *animal_vec = zoo.entry();

  // take a snapshot
  shared_ptr<ak::Content> array = animal_vec.snapshot();

  cout << array.get()-> tojson(false,1);


  
  //cute trap
  if(!rf){
    std::cout << "Cannot open file!" << std::endl;
    return 1;
    }

  //init array
  ak::ArrayBuilder animal(ak::ArrayBuilderOptions(1024, 2.0));

  //read until end of file
  //while (rf.peek() != EOF){
  while(!m__io.is_eof()) {

    // read function loop

    // start record for i-th animal
    animal.beginrecord();

    // get length of species name
    char species_len;
    rf.read(&species_len,1);
    assert(!rf.eof());

    // get species name
    char name[(int)species_len];
    rf.read(&name[0], (int)species_len);
    assert(!rf.eof());
    animal.field_check("Name");
    animal.string(name);
  
    // get age
    char age_char;
    rf.read(&age_char,1);
    assert(!rf.eof());
    animal.field_check("Age");
    animal.integer((int)age_char);

    // get weight
    char weight_char[2];
    rf.read(&weight_char[0],2);
    assert(!rf.eof());
    animal.field_check("Weight");
    animal.integer((int)  weight_char[0]+(100*weight_char[1]));

    // end record for i-th animal
    animal.endrecord();
  }
  
  // snapshot the FillableArray
  std::shared_ptr<ak::Content> array = animal.snapshot();
  std::cout << array.get()-> tojson(false,1);

  return animal;
}
