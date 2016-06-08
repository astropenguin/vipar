#!/bin/bash

# setup.sh - build Vipar tasks
# author: Akio Taniguchi (IoA, UT)

# Step 0: is CASA installed?
if ! [ `which casapy` ]; then
    echo "ERROR: CASA is not installed and/or symlinks are not created"
    echo "Please install CASA and then !create-symlinks on CASA prompt"
    exit
fi

# Step 1: build Vipar tasks
here=`pwd`
cd ${here}/tasks
echo "building Vipar tasks. this may take a while ..."
buildmytasks -o=../vipar.py

# Step 2: loading tasks on CASA startup
echo "execfile('${here}/vipar.py')" >> ~/.casa/init.py
echo "done!"
