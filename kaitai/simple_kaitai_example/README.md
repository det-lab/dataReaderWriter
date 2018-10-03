## A Simple Kaitai Example

An extremely naive example is included here to demonstrate the usage of Kaitai Struct in building a data format from scratch. It can also act as a test for your installation of the kaitai-struct-compiler and/or kaitai-struct-visualizer. The folder includes the following items:

* `ksy/animal.ksy`
  This is a simple .ksy file that describes a binary format. The structure is fairly contrived but it provides an easy introduction into Katai. The example describes a file that contains a sequence of entries with each representing an animal. Each animal has a species, an age, and a weight associated with it.

* `data/animal_raw`
  A binary file containing entries in the format described in animal.ksy

* `src/`
    Folder containing the source code that you will compile to run the example.

  - `main.cpp`
    A simple program for reading the contents of the file and writing the data to standard output.

  - `kaitai/`
    Folder containing C++ wrapper code (as provided by Kaitai) for interfacing with C++ stream libraries. These are needed to correctly compile and execute your program but you *shouldn't* have to make any changes.
    
* `bin/`
  Destination directory for compiled executable

* `setup.sh`
  Shell script to compile source code and organize resulting files

* `run.sh`
  Shell script to run the example.


## Data Format

As noted, the data file contains a animal species, age, and weight. The actual format of the binary file is slightly more complicated. The first byte of an entry contains an integer value denoting the number of letters in the species name. The next N-bytes are ascii values containing the species name. After the ascii characters, there is one byte corresponding to the age, and finally two bytes for the weight. Fields larger than one byte are written in little endian format (in this case just the weight). An example with one entry to illustrate is below:

| Bits  | 0 - 7 | 8 - 15 | 16 - 23 |  24 - 31 | 32 - 39 | 40 - 55 |
| ----- |:-----:|:------:|:-------:|:--------:|:-------:|:-------:|
| Value | 0x03  | 0x63   | 0x6f    |  0x77    | 0x06    | 0xDC05  |

If you don't have a hex chart handy; this entry is a 6 year old cow that weighs 1500lbs.


## Running the Example

This example assumes that you have installed the Kaitai Struct Compiler and was run on Ubuntu 16.04 using the *g++* and *make* utilities. It should adapt to other Linux environments with little to no modification. Instructions for compiling on Windows are included below but have not been extensively tested and are not recommended.

1. First, you need to generate the C++ code corresponding to the .ksy file. From a bash window, navigate to the `simple_kaitai_example/` directory and execute:

  ```
  $ kaitai-struct-compiler -t cpp_stl ksy/animal.ksy
  ```

  This command is fairly straightforward, the -t flag designates what target language to generate code for (i.e. c++) and the final option is the .ksy file to use to generate the code. This should generate a `animal.h` and `animal.cpp` in your working directory. Now you have everything you need to easily interact with a binary file.

2. The next step is to compile the source code and link into your program. The `main.cpp` file provided was written in advance for the example. It simply reads the binary file and echos the contents (with some formatting for readability) to standard output. You can make changes in order to experiment, but to use as-is you simply need to execute the following commands. A makefile along with two shell scripts are provided and configured to automate the process but it can be done manually as well. From the `simple_kaitai_example/` directory:

  ```
  $ ./setup.sh
  ```

  The setup script executes a makefile that compiles and links the appropriate files together to create a standalone executable.

3. Run the resulting executable:

  ```
  $ ./run.sh
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

## Running On Windows

Running the example on a Windows platform will require you to manually compile and run the program. 

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