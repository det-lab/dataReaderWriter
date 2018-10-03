# Binary Data Reader

## A library for reading and writing binary physics data into a structured format.

One of the issues currently facing the physics community is the highly variable nature of experimental data formats. Analysis software is often tightly coupled to a particular binary data format. There may be many unique formats due to the nature of experimental design, or as a byproduct of the hardware available to researchers. This means that a great analysis tool that is available might be useless to you if your data is in the incorrect format. Simplifying the process of needing to integrate a unique data format into every piece of analysis code is therefore of great value. 

This repository seeks to demonstrate and evaluate the use of existing tools to declaratively define the structure of binary data, in an effort to streamline user interaction with raw binary data. The tools currently being evaluated are Kaitai Struct and Daffodil. An extremely brief overview is given below:

### Kaitai Struct

Kaitai uses a yaml-style format to declare a binary format. The strength is that Kaitai then generates a library of code (in your language of choice) for reading a raw data file. The advantage of this is that the code can be directly included as a library into another program. See the `kaitai/` folder for more information.

### DFDL

DFDL takes a much different approach and serves directly as a parser instead of simply generating the code that the user must then incorporate. After declaring your format, DFDL parses the raw file and produces a new XML or JSON file. This file contains all the information in the raw file but has now been structure to be easily accessible. Nearly all programming languages have some type of XML or JSON parsing library which simplifies the process of accessing the relevant data. See the `dfdl/` folder for more information.