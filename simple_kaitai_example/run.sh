#!/bin/bash

EXE=bin/animalExample

if [ -e "$EXE" ]; then
    ./bin/animalExample
else
    echo "Error: /bin/animalExample does not exist"
    echo ""
    exit 1
fi