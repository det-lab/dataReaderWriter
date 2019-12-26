// BSD 3-Clause License; see https://github.com/jpivarski/awkward-1.0/blob/master/LICENSE

#include <iostream> // std::cout
#include <fstream>  // std::ifstream
#include <string>   // duh
#include <assert.h>   // for fancy erroring

#include "awkward/Slice.h"
#include "awkward/fillable/FillableArray.h"
#include "awkward/fillable/FillableOptions.h"

namespace ak = awkward;

// ideal struct
struct Animal {
  std::string species;
  int age;
  int weight;
};

// literal struct
struct Thing {
  char spec_len;
  std::string spec;
};

int main(int, char**) 
{
  std::ifstream rf("/home/josh/dev/dataReaderWriter/kaitai/simple_kaitai_example/data/animal_raw", std::ifstream::out | std::ifstream::binary);
  if(!rf){
    std::cout << "Cannot open file!" << std::endl;
    return 1;
  }
//Animal animals[3];

std::vector<Animal> animals;

//for (int i=0; i<3; i++){  
while (rf.peek() != EOF){
  Animal this_one;

  char species_len;
  rf.read(&species_len,1);
  assert(!rf.eof());
  std::cout << "Length of species name: " << (int)species_len << std::endl;

  char name[(int)species_len];
  rf.read(&name[0], (int)species_len);
  this_one.species = std::string(name);
  std::cout << "Species name: " << this_one.species << std::endl;

  char age_char;
  rf.read(&age_char,1);
  this_one.age = (int)age_char;
  std::cout << "Age: " << this_one.age << std::endl;

  char weight_char[2];
  rf.read(&weight_char[0],2);
  //this_one.weight = (int)weight_char;
  //std::cout << "\nWeight: " << this_one.weight;
  for (int i=0; i<2; i++) {std::cout << (int)weight_char[i] << " ";}
  std::cout << std::endl;

  animals.push_back(this_one);
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
}
