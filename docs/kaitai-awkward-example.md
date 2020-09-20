## A (Slightly) Awkward Kaitai Example

This directory contains files meant to demonstrate the usage Kaitai and Awkward (C++) to read custom data.  

- Note: currently, Awkward has not yet been fully implemented as a target for KSC, and KSC does not generate functional C++ files.  
As such, reference files have been handwritten to allow this example to build, and to hopefully guide future development on the Kaitai Awkward target.

* [Dependencies](#dependencies)
* [Contents](#contents)
* [Instructions](#instructions)

### Dependencies

For now:
- g++ => 9.3.0
- CMake >= 3.16
- make >= 4.2.1
- Python 3 (Anaconda is fine!)

When Awkward target is fully implemented, you will need:
- [Kaitai Struct Compiler](https://kaitai.io/#download)  ver = 0.9
- [Kaitai Struct C++ Runtime](https://github.com/kaitai-io/kaitai_struct_cpp_stl_runtime/tree/5958134ff51d629c30532004b4e50655b8763275)
- **Note that** Kaitai is still in fairly early development, so getting the right versions here is important, as breaking changes in updates are likely. We'll try to keep this updated as well, but just in case...

### Contents

* `CMakeLists.txt` and `cmake/`
  CMake instructions for generating Makefile to build program described in `src/main.cpp`. Make note of how to include Awkward and Kaitai in your own projects!

* `data/`
  A binary data file containing entries in the format described by animal.ksy (this is a symlink to `<dataRW>/data/animal_raw`)

* `src/`  
    Folder containing the source code that you will compile to run the example.

  - `main.cpp`  
    A simple example of a C++ program to read and print to stdout the contents of an `animal` format file (note - this program was handwritten, and is not generated or changed by kaitai!)

  - `animal_reference.cpp` and `animal_reference.h`
    Handwritten files that use the Kaitai Stream API to read the example data into an Awkward array

### Instructions

**Note** - This guide assumes:
- Debian/Ubuntu
- Bash
- /opt read-write access (can be done in a docker container if this is an issue! see [this dockerfile](../../docker/Dockerfile) as an example)

Dependencies / Initial Setup:

- Awkward
  ```
  git clone --recursive https://github.com/scikit-hep/awkward-1.0.git /opt/awkward-1.0 
  
  cd /opt/awkward-1.0 
  
  pip install .
  ```

- dataReaderWriter (this repo)
  ```
  cd <some working directory> 

  git clone https://github.com/det-lab/dataReaderWriter.git
  ```

- Kaitai Struct Compiler
  Installation instructions will be added when Awkward has been fully implemented as a Kaitai target

- Kaitai C++ Runtime Library
  ```
  git clone https://github.com/kaitai-io/kaitai_struct_cpp_stl_runtime.git

  mv -f kaitai_struct_cpp_stl_runtime/ dataReaderWriter/kaitai/awkward_example  
  ```
  
Building the project:

- Generate makefile
  ```
  cd dataReaderWriter/kaitai/awkward_example

  cmake -S. -Bbuild/
  ```

- Compile program 
  ```
  cd build

  make
  ```

- Run the finished product! Note that the executable takes an animal data file as an argument:
  ```
  ./kaitaiAnimalReader <dataRW dir>/data/animal_raw
  ```

The final output should look like this:
```
initiate sequence
data file found
data file converted to kaitai stream
awkward array built kaitai stream
[{"species":"cat","age":5,"weight":12},{"species":"dog","age":3,"weight":43},{"species":"turtle","age":10,"weight":5}]
```
