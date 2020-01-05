#!/bin/bash

EXE=bin/kaitaiAnimalExample

if [ -e "$EXE" ]; then
    ./"$EXE"
else
    printf "Error: \$EXE does not exist!\nPlease execute ./setup.sh to create executable"
    exit 1
fi
