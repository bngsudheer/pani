#!/usr/bin/env bash
rm -rf build
mkdir build/pani -p
cp LICENSE MANIFEST.in contributors.txt setup.py runserver.py build/pani/
cp -a pani/ build/pani
find build/ -name '*.pyc' -delete
rm -rf build/pani/pani/doc/build/ 
cd build
tar -czvf pani.tar.gz pani
cd ..
mv build/pani.tar.gz .
rm -rf build
~/workspace/pvenvs/gavika/bin/sphinx-build -b html /home/sudheer/workspace/gavika/paniweb/pani/doc/source /home/sudheer/workspace/gavika/paniweb/pani/doc/build

