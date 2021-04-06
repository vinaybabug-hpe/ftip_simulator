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

# Remove 1st argument from the
# list of command line arguments
argumentList = sys.argv[1:]
 
# Options
options = "evhl:"
 
# Long options
long_options = ["edge_file=", "help", "load", "vertex_file="]

edge_file = "edges.txt"
vertex_file = "vertices.txt"

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

        elif currentArgument in ("-v", "--vertex_file"):
            vertex_file = currentValue
             
except getopt.error as err:
    # output error, and return with an error code
    print (str(err))