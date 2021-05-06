#
#  ftipTraceConvertor.py
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
import pandas


# Configure neo4j connection string
config.DATABASE_URL = 'bolt://neo4j:test@localhost:7687'


def convert_to_csv(vertex_file, edge_file, vertex_output, edges_output) :
    print (("Loading vertices from file %s and edges from file %s") 
        % (vertex_file, edge_file))
    p1 = compile("{},={},-{}	{}")
    vertex_parser = compile("={result:^},{operator} {operands} {id}")
    vertex_parser_old=compile("{result:^},={op1:^},{operator} {op2}	{id}")
    edges_parser = compile("{}->{}")
    vertices = open(vertex_file, 'r')
    vertexLs = vertices.readlines()
    vertex_output_file=open(vertex_output, 'w')
    
    df=pandas.DataFrame(columns=['id','operand_1','operand_2','operator','result']) 
    for vertexL in vertexLs:
        temp1 = vertex_parser_old.parse(vertexL)
        # temp2 = vertex_parser.parse(vertexL)
        vertex = None
        id = None
        try:    
            if temp1:
                id=int(temp1['id'])
                result=float(temp1['result'])
                operand1=float(temp1['op1'])
                operand2=float(temp1['op2'])
                operator=temp1['operator']
                name=id
                # print(id,operand1,operand2,operator,result, sep=",", file=vertex_output_file)
                df.loc[len(df.index)]=[id,operand1,operand2,operator,result]

        except Exception as inst:
            print(type(inst))
            print("Problem with Vertex {} loading...".format(id))
    df = df.groupby(['operand_1','operand_2','operator','result'], as_index=False)['id'].apply(list).reset_index(name='related_nodes')
    df['count'] = df.apply(lambda row: len(row['related_nodes']), axis=1)
    df['id'] = df.apply(lambda row: row['related_nodes'][0], axis=1)
    vertex_dictionary={}
    for index, row in df.iterrows():
        vertex_dictionary.update(vertex_dictionary.fromkeys(row['related_nodes'], row['id']))
        related_nodes=[str(element) for element in row['related_nodes']]
        related_nodes=":".join(related_nodes)
        print(row['id'],row['id'],row['operand_1'],row['operand_2'],row['operator'],row['result'],row['count'],related_nodes, sep=",", file=vertex_output_file)   
      
    vertex_output_file.close()
    edges = open(edge_file, 'r')
    edgeLs = edges.readlines()
    edges_output_file=open(edges_output,'w')
    # print("vertex1,vertex2",file=edges_output_file)
    for edgeL in edgeLs:
        temp = edges_parser.parse(edgeL)
        from_node_id = vertex_dictionary[int(temp[0])]
        to_node_id = vertex_dictionary[int(temp[1])]
        # print(int(temp[0]),",",int(temp[1]),",CONNECTED", sep="", file=edges_output_file)    
        print(from_node_id,",",from_node_id,",CONNECTED", sep="", file=edges_output_file)    
    edges_output_file.close()

def deleteGraph():
    print("Deleting any previous graphs...")
    query = 'MATCH (n) DETACH DELETE n'
    db.cypher_query(query)
