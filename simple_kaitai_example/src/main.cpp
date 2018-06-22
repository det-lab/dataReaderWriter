
#include <fstream>
#include <iostream>
#include "animal.h" /* need to include the animal header file we generated */

using namespace std;


int main() {

  /* Open the input file in binary mode */
  ifstream infile("animal_raw", ifstream::binary);

  /* Create a kaitai stream of the source file */
  kaitai::kstream ks(&infile);

  /* Create an object from the kaitai stream, this object class is what was
     generated from using the kaitai-struct-compiler on the animal.ksy file */
  animal_t zoo = animal_t(&ks);

  /* Get a pointer to the vector containing all the animals */
  vector<animal_t::animal_entry_t*> *animal_vec = zoo.entry();

  /* Loop over the vector of animal entries, print the species, age, weight */
  for (int i = 0; i < animal_vec->size(); i++) {

    animal_t::animal_entry_t *testAnimal = animal_vec->at(i);

    cout << "Species: " << testAnimal->species() << endl;
    cout << "Age: " << static_cast<int>(testAnimal->age()) << endl;
    cout << "Weight: " << testAnimal->weight() << endl;
  }


}
