# Kaitai Struct Compiler

## Install guide for devs (ASSUMES DEBIAN)

OPTIONAL - START IN DOCKER CONTAINER

Run container:
```
$ docker run --rm -it glasslabs/awkward-kaitai
```
1. Initial container setup:
	
	a. make usable
	```
	$ apt update -y && apt upgrade -y
	$ apt install -y git sudo gnupg cmake wget gcc g++
	$ echo "Set disable_coredump false" >> /etc/sudo.conf
	```

	a. Install anaconda and cmake
	```
	$ wget --quiet https://repo.anaconda.com/archive/Anaconda3-2020.02-Linux-x86_64.sh -O /opt/anaconda.sh && /bin/bash /opt/anaconda.sh -b -p /opt/anaconda3
	$ 
	```

	b. ```git clone --recursive https://github.com/scikit-hep/awkward-1.0.git && python setup.py install --user```

### KAITAI-STRUCT-COMPILER ONLY (SKIP TO "COMPILE CODE" STEP IF NOT COMPILING KSC)

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

### COMPILE AGAINST KAITAI GENERATED (OR REFERENCE) CODE

1. Compile code using generated files

	a1. Clone data repo (if not already present from previous step)
    ```
    $ git clone https://github.com/det-lab/dataReaderWriter.git
    ```

	a2. Move into `awkward_example` directory
	```
	$ cd .../dataReaderWriter/kaitai/awkward_example
	```

	b. Run cmake
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
