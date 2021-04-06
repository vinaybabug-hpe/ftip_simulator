#
#  ftipDBLoader.py
#  This file is part of FTiP Simulator.
#
#  FTiP Simulator is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  FTiP Simulator is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with FTiP Simulator.  If not, see <https://www.gnu.org/licenses/>.
#
#

from neomodel import config, UniqueProperty, DoesNotExist, db
from parse import compile
from ftippypkg.Node import Node


# Configure neo4j connection string
config.DATABASE_URL = 'bolt://neo4j:test@localhost:7687'

def loadGraph(vertex_file, edge_file) :
    print (("Loading vertices from file %s and edges from file %s") 
        % (vertex_file, edge_file))
    p1 = compile("{},={},-{}	{}")
    p2 = compile("{},={},*{}	{}")
    p3 = compile("{},={},+{}	{}")
    pe = compile("{}->{}")
    vertices = open(vertex_file, 'r')
    vertexLs = vertices.readlines()

    for vertexL in vertexLs:
        temp1 = p1.parse(vertexL)
        temp2 = p2.parse(vertexL)
        temp3 = p3.parse(vertexL)
        vertex = None
        id = None
        try:
            if temp1:
                vertex = Node(name=temp1[3].strip("\n"), result=temp1[0], 
                operand_1=temp1[1], operand_2=temp1[2], operator="-").save()       
                id = temp1[3].strip("\n")
            
            elif temp2:
                vertex = Node(name=temp2[3].strip("\n"), result=temp2[0], 
                operand_1=temp2[1], operand_2=temp2[2], operator="*").save()
                id = temp2[3].strip("\n")
            
            elif temp3:
                vertex = Node(name=temp3[3].strip("\n"), result=temp3[0], 
                operand_1=temp3[1], operand_2=temp3[2], operator="+").save()
                id = temp3[3].strip("\n")

            print("Vertex {} loaded...".format(id))
        
        except UniqueProperty:
            print("Problem with Vertex {} loading...".format(id))
    
    edges = open(edge_file, 'r')
    edgeLs = edges.readlines()

    for edgeL in edgeLs:
        temp = pe.parse(edgeL)
        print("{}->{}".format(temp[0], temp[1]))
        edgeU = Node.nodes.get(name=temp[0].strip("\n"))
        edgeV = Node.nodes.get(name=temp[1].strip("\n"))
        edgeU.directed_edges.connect(edgeV)

def deleteGraph():
    print("Deleting any previous graphs...")
    query = 'MATCH (n) DETACH DELETE n'
    db.cypher_query(query)