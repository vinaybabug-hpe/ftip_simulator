#!/bin/bash -x

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


#podman ps -aq --filter "name=ftipneo4j0" | grep -q . && podman stop ftipneo4j0 && podman rm -fv ftipneo4j0
#podman ps -aq --filter "name=ftipneo4j" | grep -q . && podman stop ftipneo4j && podman rm -fv ftipneo4j

#podman pod rm -a -f
#podman image prune -a -f
#podman rmi -a -f

#podman run \
#--name ftipneo4j0 \
#-p7474:7474 -p7687:7687 \
#-d \
#-v $(pwd)/neo4j/data:/data \
#-v $(pwd)/neo4j/logs:/logs \
#-v $(pwd)/neo4j/import:/import \
#-v $(pwd)/neo4j/plugins:/plugins \
#--env NEO4J_AUTH=neo4j/test \
#neo4j:latest &
#--env NEO4JLABS_PLUGINS='["graph-data-science"]' \
#--env NEO4J_dbms_security_procedures_unrestricted=gds.* \
#--env NEO4J_dbms_security_procedures_whitelist=gds.* \


sleep 3

echo "Importing data"
#CONTAINER_ID=$(podman ps --format json | jq -r .[].Id)
#podman exec $CONTAINER_ID neo4j-admin import --database=ftip --nodes=Node=/import/vertex_headers.csv,/import/vertices.csv --relationships=IS_CONNECTED=/import/edge_headers.csv,/import/edges.csv
neo4j-admin import --force --database=neo4j --nodes=Node=neo4j/import/vertex_headers.csv,neo4j/import/vertices.csv --relationships=IS_CONNECTED=neo4j/import/edge_headers.csv,neo4j/import/edges.csv

#sleep 15
echo $PWD

#python3 ../ftip_sim.py --load=2


#echo "To access the graph, change connection type from neo4j to bolt and connection url to localhost:7687. The username is neo4j and the #password is test. Firefox will launch to localhost:7474/browser/ in a few seconds. You might have to refresh the page."
#sleep 8
#firefox localhost:7474/browser/

#python3 ftip_sim.py --minbandwidth=1024
