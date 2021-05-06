#
#  ftip_sim.py
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
# Python program to handle FTiP command line arguments.


import getopt, sys
from ftippypkg import ftipDBLoader as ftipdb
from ftippypkg import ftipTraceConvertor as convertor

def remove_duplicates(vertices_file)
    df = pandas.read_csv(vertices_file,header=0)
    df.groupby(['operand_1','operand_2','operator','result'], as_index=False)['id'].apply(list).reset_index(name='related_nodes')
    print(len(p.loc[24, 'related_nodes']))
    p2['count'] = p2.apply(lambda row: len(row['related_nodes']), axis=1)
    p2['id'] = p2.apply(lambda row: row['related_nodes'][0], axis=1)
    p3['related_nodes'] = p3.apply(lambda row: row['related_nodes'][1:], axis=1)
    for index, row in p2.iterrows():
        myDict.update(dict.fromkeys(row['related_nodes'], row['id']))



#
#  ftip_sim.py
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
# Python program to handle FTiP command line arguments.


import getopt, sys
from ftippypkg import ftipDBLoader as ftipdb
from ftippypkg.GraphBandwidthRecognition import BandwidthTesting as bw 
from ftippypkg import ftipTraceConvertor as convertor

# Remove 1st argument from the
# list of command line arguments
argumentList = sys.argv[1:]
 
# Options
options = "evhlcdfm:"
 
# Long options
long_options = ["edgefile=", "help", "load", "vertexfile=", "minbandwidth"]

edge_file = "edges.txt"
vertex_file = "vertices.txt"

edge_file_output = "edges_output.csv"
vertex_file_output = "vertices_output.csv"
conversion_format="csv"

try:
    # Parsing argument
    arguments, values = getopt.getopt(argumentList, options, long_options)

    # checking each argument
    for currentArgument, currentValue in arguments:
 
        if currentArgument in ("-e", "--edge_file"):
            edge_file = currentValue
             
        elif currentArgument in ("-h", "--Help"):
            print("Usage:") 
            print(("\t%s --e <edge_file_path> --v <vertex_file_path> <operation>") % (sys.argv[0]))
             
        elif currentArgument in ("-l", "--load"):
            # clear any previous graphs
            ftipdb.deleteGraph()
            # load new vertices and edges
            ftipdb.loadGraph(vertex_file, edge_file)

        elif currentArgument in ("-m", "--minbandwidth"):
            # find the minimum bandwidth of loaded graph
            bw.findBandwidth()

        elif currentArgument in ("-c", "--convert"):
            convertor.convert_to_csv(vertex_file, edge_file,vertex_file_output,edge_file_output)

        elif currentArgument in ("-d", "--edge_output"):
            edge_file_output = currentValue

        elif currentArgument in ("-f", "--vertex_output"):
            vertex_file_output = currentValue

        elif currentArgument in ("-v", "--vertex_file"):
            vertex_file = currentValue
             
except getopt.error as err:
    # output error, and return with an error code
    print (str(err))
