# Kaitai Struct

This library makes use of Kaitai Struct, documentation and download available [here](http://kaitai.io/ "Kaitai Struct"). To install and use Kaitai Struct you will need to have the Java Development Kit and Java Runtime Environment installed on your machine. Kaitai is a declarative tool for describing binary data formats.

## Kaitai Features

A Kaitai Struct download provides two main tools in order to develop the code associated with your data format.

1. Kaitai-Struct-Compiler: The compiler performs the heavy lifting and generates the source code associated with your format. It takes a user-created  .ksy file and creates the code (in a language specified by the user) for interacting with the binary data.


2. Kaitai-Struct-Visualizer: The visualizer is installed as a ruby gem (and as such requires a Ruby interpreter on your machine) and is primarily used as a debugging tool for your data descriptor. It takes a binary file and your .ksy file as inputs and creates an interactive visual representation of the format.


## Kaitai Resources

  * See `simple_kaitai_example/` for a worked example, or visit the [Kaitai Struct Documentation](https://doc.kaitai.io/user_guide.html).

  * Kaitai also has an interactive [webIDE](https://ide.kaitai.io/) with examples of many popular data/file formats.


## Sample Structures for Binary Data

This respository contains two examples of how to define a format using Kaitai Struct. The first example is in the `simple_kaitai_example/` and describes a very simple example. Use of Kaitai Struct is worked through in detail for this example.

The `scdms/` folder simply contains example .ksy files for a more complicated binary format resulting from a nuclear physics data acquisition system.