
#include <fstream>
#include <iostream>
#include "animal.h" /* need to include the animal header file we generated */

using namespace std;
namespace ak = awkward;

int main() {

  /* Open the input file in binary mode */
  ifstream infile("data/animal_raw", ifstream::binary);

  /* Create a kaitai stream of the source file */
  kaitai::kstream ks(&infile);

  /* Create an object from the kaitai stream, this object class is what was
     generated from using the kaitai-struct-compiler on the animal.ksy file */
  animal_t zoo = animal_t(&ks);

  /* Get a pointer to the vector containing all the animals */
  ak::FillableArray animal_vec = zoo.entry();
  //vector<animal_t::animal_entry_t*> *animal_vec = zoo.entry();

  // take a snapshot
  shared_ptr<ak::Content> array = animal_vec.snapshot();
 
  cout << array.get()-> tojson(false,1);

  // check output
//  if (array.get()->tojson(false,1) != "[{\"one\":true,\"two\":1,\"three\":1.1},{\"one\":false,\"two\":2,\"three\":2.2},{\"one\":true,\"two\":3,\"three\":3.3}]")
//    {return -1;}
//  return 0;


  /* Loop over the vector of animal entries, print the species, age, weight */
//  for (int i = 0; i < animal_vec.size(); i++) {
//
//    animal_t::animal_entry_t *testAnimal = animal_vec.at(i);
//
//    cout << "Species: " << testAnimal->species() << endl;
//    cout << "Age: " << static_cast<int>(testAnimal->age()) << endl;
//    cout << "Weight: " << testAnimal->weight() << endl;
//  }


}
