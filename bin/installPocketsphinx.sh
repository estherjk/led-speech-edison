#!/bin/sh

mkdir -p ../install
cd ../install

echo "Downloading pocketsphinx..."
wget http://sourceforge.net/projects/cmusphinx/files/pocketsphinx/0.8/pocketsphinx-0.8.tar.gz
tar -xvf pocketsphinx-0.8.tar.gz
rm pocketsphinx-0.8.tar.gz
cd pocketsphinx-0.8

# Remove pocketsphinx.c -- needs to be generated on the build for Edison
rm python/pocketsphinx.c

echo "Installing pocketsphinx..."
./configure
make
make install

echo "Installing Python bindings..."
cd python
python setup.py install

echo "Pocketsphinx installed."
