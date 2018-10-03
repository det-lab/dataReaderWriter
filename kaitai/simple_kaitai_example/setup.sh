#!/bin/bash

CPP=animal.cpp
HEADER=animal.h
EXE=animalExample

if [ -e "$CPP" ] && [ -e "$HEADER" ]; then
    mv animal.cpp src/
    mv animal.h src/
else 
    if ! [ -e src/"$CPP" ] || ! [ -e src/"$HEADER" ]; then
    echo "$CPP or $HEADER do not exist. Please first execute:"
    echo "\$ kaitai-struct-compiler -t cpp_stl ksy/animal.ksy"
    exit 1
    fi
fi

# run the make command to compile and link source files.
# The target in makefile is animalExample, hence
# the name of the EXE variable
make -f makefile

# Move resulting executable to bin/ directory
if [ -e "$EXE" ]; then
    mv animalExample bin/
    rm *.o # remove intermediate object files generated from makefile
    echo "Build Successful. To execute program run: ./run.sh"
fi