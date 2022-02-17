#!/bin/bash -x

CMAKE_PATH=/usr/local/bin/
export PATH=$PATH:$CMAKE_PATH
rm -rf build
mkdir build
cp vertex_headers.csv build/
cp edge_headers.csv build/

cd build
cmake ../
cp ../desc.txt ./src/desc.txt
cp ../data.csv ./src/data.csv
make
./src/kmeans ./src/desc.txt ./src/data.csv
#echo "Converting trace files. This might take a few seconds depending on data size"



rm -rf neo4j
mkdir neo4j
mkdir neo4j/import
mkdir neo4j/data
mkdir neo4j/plugins
mkdir neo4j/logs
#cp neo4j_plugins/* neo4j/plugins/ 
cp vertex_headers.csv neo4j/import/
cp edge_headers.csv neo4j/import/
cp vertices.csv neo4j/import/
cp edges.csv neo4j/import/

neo4j stop
sleep 10
echo "Importing data"


#neo4j-admin import --force --database=neo4j --nodes=Node=neo4j/import/vertex_headers.csv,neo4j/import/vertices.csv --relationships=IS_CONNECTED=neo4j/import/edge_headers.csv,neo4j/import/edges.csv
neo4j-admin import --force --database=neo4j --nodes=Node=~/Workspace/ftip_simulator/build/neo4j/import/vertex_headers.csv,~/Workspace/ftip_simulator/build/neo4j/import/vertices.csv --relationships=IS_CONNECTED=~/Workspace/ftip_simulator/build/neo4j/import/edge_headers.csv,~/Workspace/ftip_simulator/build/neo4j/import/edges.csv
neo4j start
sleep 5
echo "Done..."
