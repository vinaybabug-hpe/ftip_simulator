#!/usr/bin/env bash
rm -rf build
mkdir build 
cd build
cmake ../ 
cmake --build .
cd ..
echo 'Generating CU''s from kmeans algorithm!'
./build/src/kmeans desc.txt data.csv
