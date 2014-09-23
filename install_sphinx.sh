#!/bin/bash
set -e
rm -r build-sphinx || true
mkdir build-sphinx
cd build-sphinx
wget https://bitbucket.org/birkenfeld/sphinx/get/default.zip
unzip default.zip
cd *sphinx*
python setup.py install --user
