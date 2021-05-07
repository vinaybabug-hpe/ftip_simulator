#!/bin/bash -x

#rm -r build
#mkdir build
#cd build
#cmake -build ../
#make
#./src/kmeans
#echo "Converting trace files. This might take a few seconds depending on data size"
#python3 ../ftip_sim.py -c e
#cd ..


sudo rm -r neo4j
mkdir neo4j
mkdir neo4j/import
mkdir neo4j/data
mkdir neo4j/plugins
mkdir neo4j/logs
cp vertex_headers.csv neo4j/import/
cp edges_headers.csv neo4j/import/
cp build/vertices_output.csv neo4j/import/
cp build/edges_output.csv neo4j/import/
import_directory=$(pwd)/neo4j/import/
data_directory=$(pwd)/neo4j/data/
plugins_directory=$(pwd)/neo4j/plugins/
logs_directory=$(pwd)/neo4j/logs/

sudo docker container stop ftipneo4j
sudo docker container rm ftipneo4j

sudo docker run \
--name ftipneo4j0 \
-p7474:7474 -p7687:7687 \
-d \
-v $(pwd)/neo4j/data:/data \
-v $(pwd)/neo4j/logs:/logs \
-v $(pwd)/neo4j/import:/import \
-v $(pwd)/neo4j/plugins:/plugins \
--env NEO4J_AUTH=neo4j/test \
neo4j:latest

sleep 3

echo "Importing data"

sudo docker exec --interactive --tty ftipneo4j0 neo4j-admin import --database=neo4j2 --nodes=Nodes=/import/vertex_headers.csv,/import/vertices_output.csv --relationships=CONNECTED=/import/edges_headers.csv,/import/edges_output.csv

sleep 15

sudo docker container stop ftipneo4j0
sleep 3
sudo docker container rm ftipneo4j0
sleep 1

sudo docker run \
--name ftipneo4j \
-p7474:7474 -p7687:7687 \
-d \
-v $(pwd)/neo4j/data:/data \
-v $(pwd)/neo4j/logs:/logs \
-v $(pwd)/neo4j/import:/import \
-v $(pwd)/neo4j/plugins:/plugins \
--env NEO4J_AUTH=neo4j/test \
--env NEO4J_dbms_active__database=neo4j2 \
neo4j:latest

echo "To access the graph, change connection type from neo4j to bolt and connection url to localhost:7687. The username is neo4j and the password is test. Firefox will launch to localhost:7474/browser/ in a few seconds. You might have to refresh the page."
sleep 8
firefox localhost:7474/browser/

