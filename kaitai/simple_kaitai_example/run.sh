#!/bin/bash

EXE=bin/animalExample

if [ -e "$EXE" ]; then
    ./bin/animalExample
else
    echo "Error: /bin/animalExample does not exist"
    echo "Please execute ./setup.sh to create executable"
    echo ""
    exit 1
fi