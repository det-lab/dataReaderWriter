# Kaitai Struct

### Overview 

Kaitai Struct is a set of data-interfacing tools which can generate code in several languages, based on a description of the data structure - a Kaitai Struct YAML (.ksy) file.  
- [Kaitai download and quickstart instructions](http://kaitai.io)  
- [Kaitai Struct User Guide](https://doc.kaitai.io/user_guide.html)

Available Kaitai Struct tools include:

* [Kaitai-Struct-Compiler (KSC)](http://kaitai.io/#download): The compiler performs the heavy lifting and generates the source code associated with your format. It takes a user-created .ksy file and creates the code (in a language specified by the user) for interacting with the binary data.

* [Kaitai Stream API](http://doc.kaitai.io/stream_api.html): These libraries allow Kaitai to interface with various languages in order to generate the necessary code in the desired target language, acting essentially as a wrapper for your target language's native IO libraries. (Available as [kaitai-io github repositories](https://github.com/kaitai-io?utf8=✓&q=runtime)).
  - Note that these are required in order to implement ksc-generated code as a library into a project. 
  - Interpreted languages such as Python and Ruby require the installation of the kaitaistream package.
  - Compiled languages like C++ require compilation from source 

* [Kaitai-Struct-Visualizer (KSV)](https://github.com/kaitai-io/kaitai_struct_visualizer): The visualizer is installed as a ruby gem (and as such requires a Ruby interpreter on your machine) and is primarily used as a debugging tool for your data descriptor. It takes a binary file and your .ksy file as inputs and creates an interactive visual representation of the format.

* [Kaitai interactive webIDE](https://ide.kaitai.io/) with examples of many popular data/file formats. You can also import your own .ksy schema format and corresponding data file into the tool.

### Contents

* `simple_example/`  
  A directory containing a simplified guide to using Kaitai Struct to read binary data into C++ std vectors. Includes pre-written example code as well as instructions to generate code with ksc (kaitai-struct-compiler).

* `awkward_example/`
  An example program using Kaitai to read binary data into Awkward arrays (C++/python compatible).  
  
* `ksy/`  
  A directory containing various example kaitai struct descriptions

  - `animal.ksy`  
  A simplified data structure with some basic information about animals (species, age, and weight). Used in the `simple_example` 

  - `scdms.ksy` and `midas.ksy`  
  The ksy/scdms.ksy and ksy/midas.ksy files are an example of how to declare a more complicated custom binary format. These demonstrate a number of the capabilities of Kaitai Struct including the ability to parse packed integer values, enumerated values, and conditional statements. Additionally it demonstrates the ability to import formats described in other files since the actual data is contained in the scdms.ksy format which is then encapsulated within the midas.ksy structure.  
 Note: an example program for these have not yet been written, but you can find some `scdms_raw.bin` data in `<dataReaderWriter>/data`. Test your Kaitai knowledge by writing up a basic program similar to the `simple_example`!
