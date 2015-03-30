#!/bin/sh

mkdir -p ../install
cd ../install

echo "Downloading sphinxbase..."
wget http://downloads.sourceforge.net/project/cmusphinx/sphinxbase/0.8/sphinxbase-0.8.tar.gz
tar -xvf sphinxbase-0.8.tar.gz
rm sphinxbase-0.8.tar.gz
cd sphinxbase-0.8

# Remove sphinxbase.c -- needs to be generated on the build for Edison
rm python/sphinxbase.c

echo "Installing sphinxbase..."
./configure
make
make install

echo "Installing Python bindings..."
cd python
python setup.py install

echo "Sphinxbase installed."
