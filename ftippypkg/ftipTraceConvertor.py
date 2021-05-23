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
import numpy
import csv

# Configure neo4j connection string
config.DATABASE_URL = 'bolt://neo4j:test@localhost:7687'


def convert_to_csv(vertex_file, edge_file, vertex_output, edges_output, k=-1, parse=False):
    print(("Loading vertices from file %s and edges from file %s")
          % (vertex_file, edge_file))

    vertex_parser = compile("={result:^},{operator} {operands} {id}")
    vertex_parser_old = compile("{result:^},={op1:^},{operator} {op2}	{id}")
    edges_parser = compile("{}->{}")
    vertices = open(vertex_file, 'r')
    vertexLs = vertices.readlines()
    vertex_output_file = open(vertex_output, 'w')
    vertex_output_original_file = open("vertex_output_original.csv", 'w')

    myList=[]
    # df = pandas.DataFrame(columns=['id', 'operand_1', 'operand_2', 'operator', 'result'])
    for vertexL in vertexLs:
        
        temp1 = vertex_parser_old.parse(vertexL)
	
        vertex = None
        node_id = None
        try:
            if temp1:
                node_id = int(temp1['id'])
                result = float(temp1['result'])
                operand1 = float(temp1['op1'])
                operand2 = float(temp1['op2'])
                operator = temp1['operator']
                name = node_id
                
                # df.loc[len(df.index)] = [node_id, operand1, operand2, operator, result] 
                
                myList.append([node_id, operand1, operand2, operator, result, 1])
                
        except Exception as inst:
            print(type(inst))
            print("Problem with Vertex {} loading...".format(node_id))

    df = pandas.DataFrame(myList,columns=['id', 'operand_1', 'operand_2', 'operator', 'result', "count"])
    
    print("Manipulating dataframe")
    #df = df.groupby(['operand_1', 'operand_2', 'operator', 'result'], as_index=False)['id'].apply(list).reset_index(
        #name='related_nodes')
    #df['count'] = df.apply(lambda row: len(row['related_nodes']), axis=1)
    #df['id'] = df.apply(lambda row: row['related_nodes'][0], axis=1)

    
    print("Creating dictionary of redundant ids")
    vertex_dictionary = {}
    k = int(k)

    

    if k==0:
        for index, row in df.iterrows():
            vertex_dictionary[row['id']] = row['id']  
            # vertex_dictionary.update(vertex_dictionary.fromkeys(row['id'], row['id']))
            print(row['id'], row['id'], row['operand_1'], row['operand_2'], row['operator'], row['result'],
                  row['count'], sep=",", file=vertex_output_file)
   
    elif k < 0:
        df = df.groupby(['operand_1', 'operand_2', 'operator', 'result'], as_index=False)['id'].apply(list).reset_index(
            name='related_nodes')
        df['count'] = df.apply(lambda row: len(row['related_nodes']), axis=1)
        df['id'] = df.apply(lambda row: row['related_nodes'][0], axis=1)
        

        for index, row in df.iterrows():
           vertex_dictionary.update(vertex_dictionary.fromkeys(row['related_nodes'], row['id']))
           print(row['id'], row['id'], row['operand_1'], row['operand_2'], row['operator'], row['result'],
                 row['count'], sep=",", file=vertex_output_file)
    elif k > 0:
        df = df.groupby(['operand_1', 'operand_2', 'operator', 'result'], as_index=False)['id'].apply(list).reset_index(
            name='related_nodes')
        df['count'] = df.apply(lambda row: len(row['related_nodes']), axis=1)
        df['id'] = df.apply(lambda row: row['related_nodes'][0], axis=1)
        column_indices = {i: df.columns.get_loc(i) + 1 for i in df.columns}
        for row in df.itertuples():

            # related_nodes_list=row['related_nodes']
            related_nodes_list = row[column_indices['related_nodes']]
            node_chunks = [related_nodes_list[x:x + k] for x in range(0, len(related_nodes_list), k)]
            for node_chunk in node_chunks:
                chunk_id = node_chunk[0]
                chunk_count = len(node_chunk)
                vertex_dictionary.update(vertex_dictionary.fromkeys(node_chunk, chunk_id))
                print(chunk_id, chunk_id, row[column_indices['operand_1']], row[column_indices['operand_2']],
                      row[column_indices['operator']], row[column_indices['result']], chunk_count, sep=",",
                      file=vertex_output_file)
    vertex_output_file.close()

    edges = open(edge_file, 'r')
    edgeLs = edges.readlines()
    edges_output_file = open(edges_output, 'w')

    print("Converting id of redundant nodes to the id of the first node")
    edges_df = pandas.DataFrame(columns=['from_node', 'to_node'])
    myEdgeList=[]
    for edgeL in edgeLs:
        temp = edges_parser.parse(edgeL)
        from_node_id = vertex_dictionary[int(temp[0])]
        to_node_id = vertex_dictionary[int(temp[1])]
        #edges_df.loc[len(edges_df.index)] = [from_node_id, to_node_id]
        myEdgeList.append([from_node_id, to_node_id])


    edges_df = pandas.DataFrame(myEdgeList,columns=['from_node', 'to_node'])
    edges_df = edges_df.groupby(['from_node', 'to_node'], as_index=False).size().reset_index(name='num_relationships')
    edges_df['type'] = "CONNECTED"
    edges_df = edges_df[['from_node', 'num_relationships', 'to_node', 'type']]
    edges_df.to_csv(path_or_buf=edges_output_file, sep=',', header=False, index=False)
    edges_output_file.close()


def deleteGraph():
    print("Deleting any previous graphs...")
    query = 'MATCH (n) DETACH DELETE n'
    db.cypher_query(query)
