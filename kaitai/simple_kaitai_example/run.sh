#!/bin/bash

EXE=bin/kaitaiAnimalExample

if [ -e "$EXE" ]; then
    ./"$EXE"
else
    echo "Error: $EXE does not exist"
    echo "Please execute ./setup.sh to create executable"
    echo ""
    exit 1
fi