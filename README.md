# Binary Data Reader

### A library for reading and writing binary physics data into a structured format.

This library seeks to provide a simplified interface in order to utilize data analysis tools. One of the issues with using physics analysis software is that it is highly dependent on the format of the data that was taken. There may be many unique formats due to the nature of experimental design, or as a byproduct of the hardware available to researchers. This means that a great analysis tool that is available might be useless to you if you data is in the incorrect format.  

### Kaitai Struct

This library makes use of Kaitai Struct, available [here](http://kaitai.io/ "Kaitai Struct"). To install and use Kaitai Struct you will need to have the Java Development Kit and Java Runtime Environment installed on your machine. Kaitai is a declarative tool for describing binary data formats.


#### Using Kaitai Struct

Kaitai provides two tools in order to develop the code associated with your data format.

1. Kaitai-Struct-Compiler: The compiler performs the heavy lifting and generates the source code associated with your format. It takes a user-created  .ksy file and creates the code (in a language specified by the user) for interacting with the binary data.


2. Kaitai-Struct-Visualizer: The visualizer is installed as a ruby gem (and as such requires a Ruby interpreter on your machine) and is primarily used as a debugging tool for your data descriptor. It takes a binary file and your .ksy file as inputs and creates an interactive visual representation of the format.


#### A Simple Example

An extremely naive example is included in the `simple_kaitai_example/` folder to demonstrate the usage of Kaitai Struct in building a data format from scratch. It also acts as a test for your installation of the kaitai-struct-compiler and/or kaitai-struct-visualizer. The folder includes the following items:

* animal.ksy

  This is a simple .ksy file that describes a binary format. The structure is fairly contrived but it provides an easy introduction into Katai. The example describes a file that contains a sequence of entries with each representing an animal. Each animal has a species, an age, and a weight associated with it.

* animal_raw

  A binary file containing entries in the format described in animal.ksy

* src/

  - main.cpp

    A simple program for reading the contents of the file and writing the data to standard output.

  - kaitai/

    Folder containing C++ wrapper code (as provided by Kaitai) for interfacing with C++ stream libraries. These are needed to correctly compile and execute your program but you *shouldn't* have to make any changes.
    
    Folder containing the source code that you will compile to run the example.

* bin/

  Directory containing executable binaries

* setup.sh
  
  Shell script to compile source code and organize resulting files

* run.sh

  Shell script to run the example.


#### Running the Example

This example assumes that you have installed the Kaitai Struct Compiler and was run on Ubuntu 16.04 using the *g++* and *make* utilities. It should adapt to other Linux environments with little to no modification. Instructions for compiling on Windows are included below but have not been extensively tested and is not recommended.

1. First, you need to generate the C++ code corresponding to the .ksy file. From a bash window, navigate to the `simple_kaitai_example/` directory and execute:

  ```
  $ kaitai-struct-compiler -t cpp_stl animal.ksy
  ```

  This should generate a `animal.h` and `animal.cpp` in your working directory. Now you have everything you need to easily interact with a binary file.

2. The next step is to compile the source code and link into your program. The `main.cpp` file provided is pre-configured for the example to simply read the binary file and echo the contents to standard output. You can make changes in order to experiment, but to use as-is you simply need to execute the following commands. A makefile along with two shell scripts are provided and configured to automate this process but it can be done manually as well. From the `simple_kaitai_example/` directory:

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

#### Running On Windows

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


