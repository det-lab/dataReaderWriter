## What is Daffodil?

Daffodil is an open source implementation of the Data Format Description Language (DFDL). It builds upon the XML Schema language to provide an author a standard way to describe a variety of data formats. The DFDL specification is managed by the [Open Grid Forum](https://www.ogf.org/ogf/doku.php/standards/dfdl/dfdl "Open Grid Forum"). See the [resources](#links-to-resources) section below for more links to helpful user documentation about Daffodil as well as XML/XSD.


### SCDMS Example
***

The example presented here models a set of physics data and includes the following files:

* `data/`
  Folder containing data files corresponding to the schema.
  
  - `scdms_raw.bin`
    This is a sample set of SCDMS data in its raw binary format. <!-- You can look at the `SuperCDMS_Data_Format.xlsx` file for a description of the file structure. -->

  - `scdms_xml_data.xml`
    This xml file was previously generated using the schema definition to show what the results of a correct parse into xml looks like.


* `src/scdms/xsd/`
  Source code for schema

  - `scdms.dfdl.xsd`
    DFDL schema file that describes the data format. This is the file that Daffodil uses as a template to parse your raw binary file.

  - `config.xml`
    Configuration file to demonstrate use of tunable parameters. More information on tunables can be found at the [Daffodil Configuration](https://daffodil.apache.org/configuration/ "Apache Daffodil Configuration Documentation") documentation page.

* `src/scdms/SuperCDMS_Data_Format.xlsx`
  Excel file with an easily human-readable description of format.


#### Running the Example

To run the provided example, you first need to make sure that Java 8+ is installed on your machine. Then, download [Daffodil](https://daffodil.apache.org/ "Daffodil"). These instructions and commands are written assuming that the Daffodil folder was extracted into the `dfdl/` directory meaning your directory structure would look something like:

```
dfdl/
  |-apache-daffodil-2.2.0-incubating-bin/
    |-bin/
    |-lib/
    .
    .
    .
  |-data/
    |-scdms_raw.bin
    |-scdms_xml_data.xml
  |-src/
    |-scdms/
      |-xsd/
        |-config.xml
        |-scdms.dfdl.xsd

```

but it can be run from anywhere assuming you modify the file paths. Daffodil requires the use of Java 8 so there is only one download needed to work on either Windows/Linux.


1. First move into the Daffodil directory:

  ```
  $ cd apache-daffodil-2.2.0-incubating-bin
  ```

2. The command to parse the raw binary file into xml is:

  ```
  $ ./bin/daffodil parse -s ../src/scdms/xsd/scdms.dfdl.xsd -c ../src/scdms/xsd/config.xml -o ../data/my_xml_file.xml ../data/scdms_raw.bin
  ```

  or on Windows use the daffodil.bat script:

  ```
  > .\bin\daffodil.bat parse -s ..\src\scdms\xsd\scdms.dfdl.xsd -c ..\src\scdms\xsd\config.xml -o ..\data\my_xml_file.xml ..\data\scdms_raw.bin
  ```

3. Your output file should now be in the `data/` folder. You can compare with existing `scdms_xml_data.xml` file to see if the parse worked correctly.

4. To parse the file into JSON the command simply needs a different flag (and to change your output file extension). Daffodil defaults to xml but you need the `-I json` flag to switch to that output format.

  ```
  $ ./bin/daffodil parse -s ../src/scdms/xsd/scdms.dfdl.xsd -c ../src/scdms/xsd/config.xml -I json -o ../data/my_xml_file.json ../data/scdms_raw.bin
  ```

  and on Windows:

  ```
  > .\bin\daffodil.bat parse -s ..\src\scdms\xsd\scdms\dfdl.xsd -c ..\src\scdms\xsd\config.xml -I json -o ..\data\my_xml_file.json ..\data\scdms_raw.bin
  ```

### Links to Resources
***

#### XML and XML Schema

DFDL is built on top of eXtensible Markup Language (XML) and XML Schema (XSD). It provides an extra set of attributes that allows an author to define data formats with much more granularity and nuance. Because of this, a basic understanding of XML and XSD is necessary to begin writing (and understanding) your own schema.

* [XML Tutorial](https://www.w3schools.com/xml/default.asp "W3 Schools XML")
* [XML Schema](https://www.w3schools.com/xml/schema_intro.asp "W3 Schools XSD")

#### Current Specification

As of this writing, the Data Format Description Language v1.0 standard is defined in GFD-P-R.207. 

* [DFDL Specification v1.0](https://www.ogf.org/documents/GFD.207.pdf "Open Grid Forum DFDL Specification")

#### Daffodil

Daffodil is currently under development as an Apache Incubator project. Documentation and downloads can be found at <https://daffodil.apache.org/>. This example was completed using version 2.2.0.

##### Daffodil Resources:

* [Getting Started](https://daffodil.apache.org/getting-started/) - Includes information on the command line options etc.
* [Mailing List and Community](https://daffodil.apache.org/community/) - The Daffodil community is very responsive and extremely helpful for questions.
* [Github Repository](https://github.com/apache/incubator-daffodil)
* [Examples](https://daffodil.apache.org/examples/)

### Serialization
***

Daffodil also supports the ability to serialize (unparse) data (i.e. writing an xml or json file into the binary format specified by your .dfdl.xsd schema file). This process is not covered here but more information can be found in the [Daffodil documentation](https://daffodil.apache.org/cli/ "Unparse Docs").

<!-- 
pros ==> human readable output (easy to debug)
     ==> parses available in almost all languages
     ==> json or xml outputs
     ==> reading and writing ability

cons ==> large data files become even larger
     ==> debugging format can be difficult



kaitai
pros ==> efficient
     ==> can generate code for many languages
     ==> ruby gem makes debugging much easier


cons ==> no writing capability
     ==> auto-generated code is confusing for complex formats
     ==> ksv crashes for large files -->