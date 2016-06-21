#!/bin/bash

# setup.sh - build Vipar tasks
# author: Akio Taniguchi (IoA, UT)

root=`pwd`

# Step 0: is CASA installed?
if ! [ `which casapy` ]; then
    echo "ERROR: CASA is not installed and/or symbolic links are not created"
    echo "Please install CASA and then execute !create-symlinks on a CASA prompt"
    exit
fi

# Step 1: create vipar.py for normal use
echo ""
echo "creating vipar.py ..."
echo "(this may take a while)"

cd ${root}/tasks
buildmytasks -o=../vipar.py
cd ${root}
echo "mbinit()" >> vipar.py
echo "done!"

# Step 2: create vipardev.py for development use
echo ""
echo "creating vipardev.py ..."

echo "import os, sys, glob, inspect" > vipardev.py
echo "sys.path.append('${root}/tasks')" >> vipardev.py
echo "scripts = glob.glob('${root}/tasks/task_*.py')" >> vipardev.py
echo "modules = [os.path.basename(s)[:-3] for s in scripts]" >> vipardev.py
echo "for module in modules:" >> vipardev.py
echo "    exec('from {0} import {1}'.format(module, module[5:]))" >> vipardev.py
echo "mbinit()" >> vipardev.py
echo "done!"

# Step 3: print instruction and finish setup
sleep 1.0s
echo ""
echo "setup successfully finished!"
echo "to use Vipar in CASA, execute vipar.py on a CASA prompt:"
echo "CASA <2>: execfile('${root}/vipar.py')"
echo ""
echo "(only for development use)"
echo "to use Vipar outside CASA, execute vipardev.py on a (I)Python prompt:"
echo ">>> execfile('${root}/vipardev.py')"
echo ""
