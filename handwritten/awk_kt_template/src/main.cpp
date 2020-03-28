#include <fstream>
#include <iostream>
#include "animal.h" /* need to include the animal header file we generated */

using namespace std;
namespace ak = awkward;

int main() {

  cout << "initiate sequence"<< endl; 

  /* Open the input file in binary mode */
  ifstream infile("/home/josh/dev/awkward-kaitai/dataReaderWriter/data/animal_raw", ifstream::binary);

  cout << "In-file check" << endl;

  /* Create a kaitai stream of the source file */
  kaitai::kstream ks(&infile);

  cout << "kaitai stream check" << endl;

  /* Get a pointer to the vector containing all the animals */
  ak::ArrayBuilder animal_array = _read(&ks);

  cout << "awkward array check" << endl;

  // take a snapshot
  shared_ptr<ak::Content> array = animal_array.snapshot();
 
  cout << array.get()-> tojson(false,1);

}
