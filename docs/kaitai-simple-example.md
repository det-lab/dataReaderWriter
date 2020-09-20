## A Simple Kaitai Example

This directory contains files meant to demonstrate a very simplistic usage of reading custom data using Kaitai  and C++.  
Examples of handwritten as well as Kaitai-generated code are included.  

* [Directory contents](#contents)
* [Animal data format](#data-format)
* [Instructions - Linux](#linux)
* [Instructions - Windows (not tested)](#windows)

### Dependencies

- g++
- make
- [kaitai-struct-compiler](https://kaitai.io/#download) v 0.9
- (Optional)[Kaitai Stream API](http://doc.kaitai.io/stream_api.html) runtime for your desired target language
- **NOTE:** Kaitai is still in fairly early development, so getting the right versions here is important, as breaking changes in updates are likely. We'll try to keep this updated as well, but just in case...

### Contents

* `data/animal_raw`  
  A binary data file containing entries in the format described in animal.ksy (a symlink to `<dataRW>/data/animal_raw`)

* `src/`  
    Folder containing the source code that you will compile to run the example.

  - `main.cpp`  
    A simple example of a C++ program to read and print to stdout the contents of an `animal` format file (note - this program was handwritten, and is not generated or changed by kaitai!)

  - `kaitai/`  
    This directory contains kaitai-struct's C++ runtime library, and was taken from [kaitai_struct_cpp_stl_runtime](https://github.com/kaitai-io/kaitai_struct_cpp_stl_runtime/tree/72dd2d44b53d35b8c7b493c9000d315eb6f9ff1d). This code allows Kaitai to interface with standard C++ stream libraries **and are required** to correctly compile and execute your program. You shouldn't have to make any changes to this directory, it just needs to exist and be findable when you compile your program (for example, [makefile](makefile)) lines 3 and 6).

* `makefile`  
  `make` instructions to compile the program described in `main.cpp`. Take note of how to make use of Kaitai in your own code:
  
  - line 3: this tells the compiler to link to the kaitai-struct C++ runtime library
  
  - line 6: this designates the kaitai-struct C++ runtime files as intermediate objects

  - line 9: kaitai-struct [requires that](https://doc.kaitai.io/lang_cpp_stl.html#_string_encoding) `KS_STR_ENCODING_NONE` or `KS_STR_ENCODING_ICONV` be defined at compile time

  - line 12: the main program, kaitai generated code, and kaitai stream must all be declared as objects for the target to successfully build


### Data Format

As noted, the data file contains a animal species, age, and weight. The actual format of the binary file is slightly more complicated. The first byte of an entry contains an integer value denoting the number of letters in the species name. The next N-bytes are ascii values containing the species name. After the ascii characters, there is one byte corresponding to the age, and finally two bytes for the weight. Fields larger than one byte are written in little endian format (in this case just the weight). An example with one entry to illustrate is below:

| Bits  | 0 - 7 | 8 - 15 | 16 - 23 |  24 - 31 | 32 - 39 | 40 - 55 |
| ----- |:-----:|:------:|:-------:|:--------:|:-------:|:-------:|
| Value | 0x03  | 0x63   | 0x6f    |  0x77    | 0x06    | 0xDC05  |

If you don't have a hex chart handy; this entry is a 6 year old cow that weighs 1500lbs.


## Running the Example

### Linux 

0. Move into the simple example directory:

  ```bash
  $ cd <dataReaderWriter_directory>/kaitai/simple_example`
  ```

1. First, we'll need to generate the C++ code corresponding to the .ksy file:

  ```bash
  $ kaitai-struct-compiler -t cpp_stl --outdir ./src ../ksy/animal.ksy 
  ```

  Note:  

    - The `-t` flag designates the target language (eg. c++, python, perl, etc.)  
    - The `--outdir` flag specifies the output directory for the designated code  
    - The final argument is the `.ksy` template to be used in generating the code  
    - The generated files will be automatically named as described in the `.ksy` file.  

2. Now we have a way to interact with our binary data using kaitai! Let's compile our our source code and build our program:

  ```bash
  $ make
  ```

  Recall that this `main.cpp` was pre-written as an example. Once you're convinced everything is working, you can play around with making some changes to this file, and repeating `$ make` to recompile the program and try running again. 

3. Cleanup and organization:

  ```bash
  $ mkdir bin/ && mv kaitaiAnimalExample bin/ # move executable to its own spot
  $ rm *.o # cleanup build remnants
  ```

4. Run the executable:

  ```bash
  $ ./bin/kaitaiAnimalExample
  ```  

  If everything worked correctly, you should get the following output:

  ```
    Species: cat
    Age: 5
    Weight: 12
    Species: dog
    Age: 3
    Weight: 43
    Species: turtle
    Age: 10
    Weight: 5
  ``` 

### Windows

Running the example on a Windows platform will require you to manually compile and run the program. The process is essentially the same. 

  1. Generate the source code using the Kaitai compiler as before from a command prompt:

  ```
  > kaitai-struct-compiler -t cpp_stl animal.ksy
  ```

  2. Move the resulting `animal.h` and `animal.cpp` files into the `src\` directory.

  3. Compile the code using whatever c++ compiler is available to you. For example:

  ```
  > cl \Fe: animalExample src\main.cpp src\animal.cpp src\kaitai\kaitaistream.cpp
  ```

  4. Run the program:

  ```
  > animalExample
  ```
