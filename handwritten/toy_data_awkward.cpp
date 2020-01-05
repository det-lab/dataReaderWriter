// BSD 3-Clause License; see https://github.com/jpivarski/awkward-1.0/blob/master/LICENSE

#include <iostream> // std::cout
#include <fstream>  // std::ifstream
#include <string>   // duh
#include <assert.h> // for fancy erroring

#include "awkward/Slice.h"
#include "awkward/fillable/FillableArray.h"
#include "awkward/fillable/FillableOptions.h"

namespace ak = awkward;

int main(int, char**){

  std::ifstream rf("/home/josh/dev/dataReaderWriter/kaitai/simple_kaitai_example/data/animal_raw", std::ifstream::out | std::ifstream::binary);
  if(!rf){
    std::cout << "Cannot open file!" << std::endl;
    return 1;
    }

  ak::FillableArray animals(ak::FillableOptions(1024, 2.0));

  while (rf.peek() != EOF){
  
    // start record for i-th animal
    animals.beginrecord();

    // get length of species name
    char species_len;
    rf.read(&species_len,1);
    assert(!rf.eof());

    // get species name
    char name[(int)species_len];
    rf.read(&name[0], (int)species_len);
    assert(!rf.eof());
    animals.field_check("Name");
    animals.string(name);
  
    // get age
    char age_char;
    rf.read(&age_char,1);
    assert(!rf.eof());
    animals.field_check("Age");
    animals.integer((int)age_char);

    // get weight
    char weight_char[2];
    rf.read(&weight_char[0],2);
    assert(!rf.eof());
    animals.field_check("Weight");
    animals.integer((int)  weight_char[0]+(100*weight_char[1]));

    // end record for i-th animal
    animals.endrecord();
  }
  
  // snapshot the FillableArray
  std::shared_ptr<ak::Content> array = animals.snapshot();
  std::cout << array.get()-> tojson(false,1);

  return 0;
}
////// Awkward stuff for later //////
//  create fillable array
//  ak::FillableArray myarray(ak::FillableOptions(1024, 2.0));
//  
//  // take a snapshot 
//  std::shared_ptr<ak::Content> array = myarray.snapshot();
//
//  // check output 
//  if (array.get()->tojson(false,1) != "[{\"one\":true,\"two\":1,\"three\":1.1},{\"one\":false,\"two\":2,\"three\":2.2},{\"one\":true,\"two\":3,\"three\":3.3}]")
//    {return -1;}
//  return 0;
