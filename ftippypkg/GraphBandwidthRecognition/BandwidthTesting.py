#
#  BandwidthTesting.py
#  This file is part of FTiP Simulator and implements algorithm from
#  Article,  
#  Saxe, J. B. Dynamic-programming algorithms for recognizing small-bandwidth
#  graphs in polynomial time SIAM Journal on Algebraic Discrete Methods, 
#  SIAM, 1980, 1, 363-369 
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
from ftippypkg.Node import Node
from collections import deque
from collections import namedtuple
from collections import defaultdict
import math


# Configure neo4j connection string
config.DATABASE_URL = 'bolt://neo4j:test@localhost:7687'
ActiveRegion = namedtuple("ActiveRegion", ["vertex", "examined", "unplaced"])

# Wrapper method to find bandwitdh of graph G
def findBandwidth():
    print("Find the minimum bandwidth of graph G.")
    allvertex = Node.nodes.all()
    k = 0
    
    #create connected components and determine max 2k size
    (dfsorder, _2k) = createConnectedComponents("0", len(allvertex))
    k = math.ceil(_2k/2)
    # 1. Fifo queue for active regions
    Q = deque() 
     # 2nd data structure - Array to keep track of possible active regions        
    A = defaultdict()
    successors = defaultdict()
    phiunplaced = set()  
    lk = 5
    arid = 1
    A[0] = "phi"
    print('\n==================================================================')    
    for i in range(0, len(dfsorder), lk):        
        print("\n")
        print(dfsorder[i:i+k], end=' ')
        ar = ActiveRegion(vertex=set(dfsorder[i:i+k]), examined = False, unplaced = None) 
        phiunplaced.union(ar.vertex)
        #A[arid] = ar
        #for v in A[arid-1].vertex:
        #    successors[v] = arid      

    arrv["phi"] = ActiveRegion(vertex=set(), examined = True, unplaced = phiunplaced) 
    # Initialize q_active_regions
    Q.append(arrv["phi"])
    print(isMinBandwidthK(dfsorder, 5))

    return True

#
# This method implements the Algorithm B, in section 3 of article by Saxe et al.
# Q - A Fifo queue of active regions
# A - A array of possible active regions
# Algorithm B (Bandwidth testing):
# 1. Extract an active region, r, from the head of Q
# 2 From A[r].unplaced, determin the successors of r.
# 3. For each successor, s, of r such that A[s].examined is FALSE, perform
#    the following steps:
#   
#    a. Set A[s].examined to TRUE.
#    b. Computer A[s].unplaced by deleting the last vertex of s from
#       A[r].unplaced.
#    c. If A[r].unplaced is the empty set, then halt asserting that 
#       Bandwidth(G) <= k.
#    d. Insert s at the end of Q.
#
# 4. If Q is empty, then halt asserting that Bandwidth(G) > k. Otherwise , go
#    to Step 1.
#
def isMinBandwidthK(Q : deque, A : defaultdict):
    print("Checking for minimum bandwidth of graph <= k")   

    while Q:
        curractiveregion = Q.popleft()
        unplaced = curractiveregion.unplaced
            
        r = Node.nodes.get(name=curractiveregion.vertex)
        for s in r.directed_edges:
            sar = unplaced.pop(s.name)
            if sar and sar.examined == False:
                sar.examined = True
                sarrv = defaultdict()
                for ssvertex in s.directed_edges:
                    if ssvertex.name in unplaced:
                        sarrv[ssvertex.name] =  unplaced.pop(ssvertex.name) 
                sar.unplaced = sarrv
                if not unplaced:
                    return True
            activeregionsQ.append(sar)
    return False 

def createConnectedComponents(snode: str, graphlen : int):
    startNode = Node.nodes.get(name=snode)
    visited = set()
    lk = 0
    dfsorder = []
    def dfsutil(cn):
        nonlocal lk
        # mark node visited        
        dfsorder.append(cn.name)
        visited.add(cn.name)                
        lk = max(lk, len(cn.directed_edges))
        # visit all other of current node
        for neighbor in cn.directed_edges:
            if neighbor.name not in visited:
                dfsutil(neighbor)
        return
    dfsutil(startNode)
    return (dfsorder, lk)