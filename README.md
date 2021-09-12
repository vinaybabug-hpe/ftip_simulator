# FTiPSim- Floor Tile Planning Simulator

FTiP Simulator is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

FTiP Simulator is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with FTiP Simulator.  If not, see <https://www.gnu.org/licenses/>.

FTiPSim is a tool that is used to track repeated patterns in computational steps of various clustering algorithms used in ensemble methods. FTiPSim is used to analyze patterns across local, global, single statement, code blocks, and functions over multiple invocations. The simulator starts by producing the pair (M,G), where M is an aggregation of computational units and G is the associated interaction graph. The simulator keeps track of the number of computational units, number of dependencies between those units, and computes the minimum bandwidth of G. Simulator stores data using graph database management system Neo4j, which requires creation of the following directories:

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

    Simulator uses python to interact with neo4j database. And requires driver and Neomodel.

    pip install neo4j
    pip install neomodel

    Please following link (https://neo4j.com/developer/python/) for more details.

Simulator exposes gen_graph.sh script to build custom kmeans algorithm and run it. This script uses desc.txt and data.csv to specify run parameters. These parameters are used while generating cu graph for ensemble.
To run the script type ./gen_graph.sh at the terminal.

Simulator can be used to load the graph,
    python3 ftip_sim.py --e edges.txt --v vertices.txt –l
and find minimum bandwidth of the loaded graph
    python3 ftip_sim.py --m
Please modify BandwidthTesting.py, to change behavior of algorithm used to find minimum bandwidth.
