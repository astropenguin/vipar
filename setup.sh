#!/bin/bash

# setup.sh - build Vipar tasks
# author: Akio Taniguchi (IoA, UT)

# Step 0: is CASA installed?
if ! [ `which casapy` ]; then
    echo "ERROR: CASA is not installed and/or symbolic links are not created"
    echo "Please install CASA and then execute !create-symlinks on a CASA prompt"
    exit
fi

# Step 1: build Vipar tasks
root=`pwd`
cd ${root}/tasks
echo "building Vipar tasks. this may take a while ..."
buildmytasks -o=../vipar.py

# Step 2: loading tasks on CASA startup
echo "execfile('${root}/vipar.py')" >> ~/.casa/init.py
echo "done!"
