# FTiP Simulator

FTiP Simulator is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

FTiP Simulator is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Foobar.  If not, see <https://www.gnu.org/licenses/>.
 
Simulator code for the FTiP paper.

Simulator uses Neo4j to store data. For neo4j please create following 
directories
* $HOME/neo4j/data
* $HOME/neo4j/logs
* $HOME/neo4j/import
* $HOME/neo4j/plugins 

For running neo4j in docker under linux

docker run \
    --name ftipneo4j \
    -p7474:7474 -p7687:7687 \
    -d \
    -v $HOME/neo4j/data:/data \
    -v $HOME/neo4j/logs:/logs \
    -v $HOME/neo4j/import:/var/lib/neo4j/import \
    -v $HOME/neo4j/plugins:/plugins \
    --env NEO4J_AUTH=neo4j/test \
    neo4j:latest

For running neo4j in docker under windows wsl

docker run \
    --name ftipneo4j \
    -p7474:7474 -p7687:7687 \
    -d \
    -v $HOME/neo4j/data:/data \
    -v $HOME/neo4j/logs:/logs \
    -v $HOME/neo4j/import:/var/lib/neo4j/import \
    -v $HOME/neo4j/plugins:/plugins \
    --env NEO4J_AUTH=neo4j/test \
	--env NEO4J_dbms_connector_https_advertised__address="localhost:7473" \
	--env NEO4J_dbms_connector_http_advertised__address="localhost:7474" \
	--env NEO4J_dbms_connector_bolt_advertised__address="localhost:7687" \
    neo4j:latest