# Kaitai Struct Compiler

## Install guide for devs (ASSUMES DEBIAN)

OPTIONAL - START IN DOCKER CONTAINER

Run container:
```
$ docker run --rm -it ubuntu
```
1. Initial container setup:
```
$ apt update -y && apt upgrade -y
$ apt install -y git sudo gnupg cmake 
$ echo "Set disable_coredump false" >> /etc/sudo.conf
```
1. Install Awkward and some depends:

	a. anaconda and cmake

	b. ```git clone https://github.com/scikit-hep/awkward-1.0.git && python setup.py install --user```

1. COMPILE KAITAI STRUCT COMPILER

    a. add sbt repository:
    `echo "deb https://dl.bintray.com/sbt/debian /" | sudo tee -a /etc/apt/sources.list.d/sbt.list`
    `sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 2EE0EA64E40A89B84B2DF73499E82A75642AC823`

    b. update repositories:
    `sudo apt update -y`

    c. install packages:
    `sudo apt install -y sbt default-jdk dpkg dpkg-dev lintian fakeroot`

    (Note this final apt install command may request input for region and timezone)

    d. Test sbt (optional)
    ```
    sbt test
    ```

1. Clone kaitai-struct-compiler
    ```
    git clone -b awkward --recursive https://github.com/det-lab/kaitai_struct_compiler.git
    ```
	
1. Build kaitai-struct-compiler 
    ```
    $ cd kaitai_struct_compiler
    $ sbt compilerJVM/debian:packageBin
    $ sudo dpkg -i jvm/target/kaitai-struct-compiler_0.9-SNAPSHOT_all.deb
    ```

1. Generate data-reading code

    a. Clone data repo
    ```
    $ git clone https://github.com/det-lab/dataReaderWriter.git
    ```
    
    b. Run ksc on data description
    ```
    cd dataReaderWriter/kaitai/awkward_example
    ksc -t cpp_awk ../../kaitai/ksy/animal.ksy --outdir src/
    ```
    
    c. Check generated files: `src/animal.cpp` and `src/animal.h`

1. Compile code using generated files

	a. Move into `awkward_example` directory
	```
	$ cd .../dataReaderWriter/kaitai/awkward_example
	```

	b. cmake
	```
	cmake -S. -Bbuild/ 
	```

*-----------------------------------------------------------------------------------*

- g++ -I/opt/awkward-1.0/include -L/opt/awkward-1.0/build/lib.linux-x86_64-3.7/awkward1 ../src/main.cpp -lawkward-static -lawkward-cpu-kernels-static -o kaitaiAnimalReader


#### TODO

Awkward: 
- Link libraries in program compilation

KSC:
- need to variablize:

l 215      -   m_entry
l 573      -   animal_entry_t, m__io, this, m__root
l 574-581  -   age, name, weight, etc.

- how to parse KSY file?

- open Kaitai issue
	- Separate class constructors (maybe?)

*-----------------------------------------------------------------------------------*