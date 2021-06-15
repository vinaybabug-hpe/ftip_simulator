#!/bin/bash -x

rm -r build
mkdir build

cd build
cmake -build ../
cp ../desc.txt ./src/desc.txt
cp ../data.csv ./src/data.csv
make
./src/kmeans desc_32.txt data_32.csv
#echo "Converting trace files. This might take a few seconds depending on data size"



sudo rm -r neo4j
mkdir neo4j
mkdir neo4j/import
mkdir neo4j/data
mkdir neo4j/plugins
mkdir neo4j/logs
#cp neo4j_plugins/* neo4j/plugins/ 
cp vertex_headers.csv neo4j/import/
cp edges_headers.csv neo4j/import/
cp build/vertices_output.csv neo4j/import/
cp build/edges_output.csv neo4j/import/


sudo docker ps -aq --filter "name=ftipneo4j0" | grep -q . && sudo docker stop ftipneo4j0 && sudo docker rm -fv ftipneo4j0
sudo docker ps -aq --filter "name=ftipneo4j" | grep -q . && sudo docker stop ftipneo4j && sudo docker rm -fv ftipneo4j


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
#--env NEO4JLABS_PLUGINS='["graph-data-science"]' \
#--env NEO4J_dbms_security_procedures_unrestricted=gds.* \
#--env NEO4J_dbms_security_procedures_whitelist=gds.* \


sleep 3

echo "Importing data"

sudo docker exec --interactive --tty ftipneo4j0 neo4j-admin import --database=neo4j2 --nodes=Node=/import/vertex_headers.csv,/import/vertices_output.csv --relationships=CONNECTED=/import/edges_headers.csv,/import/edges_output.csv

sleep 15
cd build
python3 ../ftip_sim.py --load=2
cd ..

#echo "To access the graph, change connection type from neo4j to bolt and connection url to localhost:7687. The username is neo4j and the #password is test. Firefox will launch to localhost:7474/browser/ in a few seconds. You might have to refresh the page."
sleep 8
firefox localhost:7474/browser/

python3 ftip_sim.py --minbandwidth=1024
