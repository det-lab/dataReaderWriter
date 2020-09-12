#include <fstream>
#include <iostream>
#include <string>
#include "animal_reference.h" /* need to include the animal header file we generated */

using namespace std;
namespace ak = awkward;

int main(int num_args, char** argv) {

  cout << "initiate sequence"<< endl; 

  /* Open the input file in binary mode */
//ifstream infile("/root/dataReaderWriter/data/animal_raw", ifstream::binary);
  string input_file(argv[1]);
  ifstream infile(input_file, ifstream::binary);

  cout << "data file found" << endl;

  /* Create a kaitai stream of the source file */
  kaitai::kstream ks(&infile);

  cout << "data file converted to kaitai stream" << endl;

  /* Get a pointer to the array containing all the animals */
  ak::ArrayBuilder animal_array = read_animal(&ks);

  cout << "awkward array built kaitai stream" << endl;

  // take a snapshot
  shared_ptr<ak::Content> array = animal_array.snapshot();
 
  cout << array.get()-> tojson(false,1);
}
