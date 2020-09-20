# Binary Data Reader

## A library for reading and writing binary physics data into a structured format.

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1479913.svg)](https://doi.org/10.5281/zenodo.1479913)

One of the issues currently facing the physics community is the highly variable nature of experimental data formats. Analysis software is often tightly coupled to a particular binary data format. There may be many unique formats due to the nature of experimental design, or as a byproduct of the hardware available to researchers. This means that a great analysis tool that is available might be useless to you if your data is in the incorrect format. Simplifying the process of needing to integrate a unique data format into every piece of analysis code is therefore of great value. 

This repository seeks to demonstrate and evaluate the use of existing tools to declaratively define the structure of binary data, in an effort to streamline user interaction with raw binary data.

## Interfacing with data

### Hand-Writing Code

Writing code by hand to interact with your binary data files is always one option. This is a great way to get a better feel for your data structure, and get an idea of how exactly you might be interested in interacting with it. Some simplistic example code can be found in the [handwritten](handwritten/) directory.  

However, it's worth being aware that this can very quickly become a tedious and titanic effort. Luckily for us, there are ways we can make computers write the code for us!

**Side note:** If you're working with hand-written code to interface with the `animal_raw` data, you may experience some weirdness with the standard output (in particular, random additional characters may be rendered along with the string "cat").

### Kaitai Struct

One code-generating option is Kaitai Struct, which uses a yaml-style format to declare a binary data format's structure. The strength is that Kaitai then generates a library of code (in your language of choice) for reading a raw data file. The advantage of this is that the code can be directly included as a library into another program. 

See the [kaitai](kaitai/) directory for [more information about kaitai](docs/kaitai-struct.md), as well as some example code using Kaitai Struct Compiler.

### DFDL

DFDL takes a much different approach and serves directly as a parser instead of simply generating the code that the user must then incorporate. After declaring your format, DFDL parses the raw file and produces a new XML or JSON file. This file contains all the information in the raw file but has now been structure to be easily accessible. Nearly all programming languages have some type of XML or JSON parsing library which simplifies the process of accessing the relevant data. 

[Click here](dfdl/README.md) for more information and a usage example on Daffodil.