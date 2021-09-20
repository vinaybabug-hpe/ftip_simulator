#
#  BandwidthTesting.py
#  This file is part of FTiP Simulator and implements algorithms from two
#  Articles,
#  Saxe, J. B. Dynamic-programming algorithms for recognizing small-bandwidth
#  graphs in polynomial time SIAM Journal on Algebraic Discrete Methods,
#  SIAM, 1980, 1, 363-369
#  Article (gurari1984improved)
#  Gurari, E. M. & Sudborough, I. H. Improved dynamic programming algorithms
#  for bandwidth minimization and the mincut linear arrangement problem
#  Journal of Algorithms, Elsevier, 1984, 5, 531-546
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


from neomodel import config, UniqueProperty, DoesNotExist, db
from neomodel import RelationshipTo
from ftippypkg.Node import Node
from collections import deque
from collections import namedtuple
from collections import defaultdict
import math


# Configure neo4j connection string
config.DATABASE_URL = 'bolt://neo4j:test@localhost:7687'
ActiveRegion = namedtuple("ActiveRegion", ["vertex", "examined", "unplaced"])
P = namedtuple('P', ['r', 'd'])

#
# Wrapper method to find bandwitdh of graph G.
# This method does a binary search over
#
def findBandwidth(graphlayoutsize : int):
    print("Find the minimum bandwidth of graph G.")
    allvertex = Node.nodes.all()
    if graphlayoutsize == "all":
        graphlayoutsize = len(allvertex)
    else:
        graphlayoutsize = int(graphlayoutsize)
    k = 0
    #create connected components / layout of G and determine max 2k size
    (dfsorder, _2k) = createConnectedComponents("0", len(allvertex))
    k = math.ceil(_2k/2)
    print("K for G is %d" % (k))
    minBandwidth = float("inf")
    # Call Bandwidth(G, k); G is subset vertices in dfsorder.
    # For small graph you can pass full graph vertices
    # Bandwidth(G) = min{bandwidth(f) | f is a layout of G
    for i in range(0, len(dfsorder), graphlayoutsize):
        low, mid, high = k, (k + len(allvertex))/2, len(allvertex)
        lrslt, mrslt, hrslt = False, False, False
        while True:
            if high >= low:
                mid = (low + (high-1))/2
                mrslt = Bandwidth(dfsorder[i:i+graphlayoutsize], mid)
                if mrslt:
                    high = mid-1
                else:
                    low = mid+1
            else:
                break
        minBandwidth = min(minBandwidth, mid)
    print("Minimum bandwidth of graph G is %d" % (minBandwidth))

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

#
# Method returns set of edges incident on v in vertices.
# It also includes dangling edges.
#
def getEdges(vertices : set):
    edges = set()
    for v in vertices:
        startNode = Node.nodes.get(name=v)
        for endNode in startNode.directed_edges:
            edges.add((startNode.name, endNode.name))
    return edges

def createConnectedComponents(snode: str, graphlen : int):
    startNode = Node.nodes.get(name=snode)
    visited = set()
    lk = 0
    dfsorder = []
    def dfsutil(cn):
        nonlocal lk
        #nonlocal edges
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

#
# Check if partial layout is K bandwidth plausible.
#
def bandwidthKplausible(p, k):
    (r, d) = p
    r = list(r)
    incident = defaultdict(int)
    for v in r:
        incident[v] = 0
    for e in d:
        for v in e:
            if v in set(r):
                incident[v] += 1
    i = len(r)
    for j in range(i):
        if incident[r[j]] <= abs(k-i+j):
            continue
        else:
            return False
    return True

#
# This method implements the Algorithm in Fig. 2.1 from
# Gurari, E. M. & Sudborough, I.H.
# The procedure Unassigned.
#
def Unassigned(R, D):
    V = set()
    Q = deque()
    DG = defaultdict(bool)
    A = defaultdict(bool)

    if not D:
        # change implementation to return vertices in a sequential array
        return {"0"}
    for e in D:
        DG[e] = True
        Q.append(e)
    for v in R:
        A[v] = True
    while Q:
        (x, y) = Q.popleft()
        z = None
        if A[x] == False or A[y] == False:
            if A[x] == False:
                z = x
            else:
                z = y
            A[z] = True
            V = V.union({z})
            Z = Node.nodes.get(name=z)
            for e in Z.directed_edges:
                if DG[e.name] == False:
                    Q.append((z, e.name))
                    DG[e.name] = True
    return V

#
# This method implements the Algorithm in Fig. 2.2 from
# Gurari, E. M. & Sudborough, I.H.
# The procedure Update.
#
def Update(p, s):
    # let p = (R, D), where R = (v1, v2,..., vi)
    # and D = (e1, e2..., ej)
    (R, D) = p
    R = list(R)
    Dtemp = D.copy()
    for e in D:
        # del e if incident on s
        Dtemp.remove(e)
    D = Dtemp
    k = 0
    if len(R) == 0 or len(R) < k:
        vk = None
    else:
        vk = R[k]
    for e in D:
    # while vk is not incident to an edge in D
    # k += 1
        if vk not in e:
            k += 1
    for e in s.directed_edges:
        if e not in R:
            D.add((s.name, e.name))
    R_temp = list()
    count = 0
    for v in R:
        if count < k:
            count += 1
            continue
        R_temp.append(v)
        count += 1
    R_temp.append(s.name)
    return P(r=set(R_temp), d=D)

#
# This method implements the Algorithm in Fig. 2.3 from
# Gurari, E. M. & Sudborough, I.H.
# An algorithm for determining if a graph G has bandwidth k
#
def Bandwidth(G, k):
    edges = getEdges(G)

    Q = deque()
    # 2. an array T which contains one element for each
    # bandwidth-kplausible pair p = (r, d).
    T = defaultdict(bool)
    p = P(r= set(), d = set())
    Q.append(p)
    while Q:
        (r, d) = Q.popleft() # p = (r, d)
        p = (r, d)
        if r and len(r) == k:
            # Get s from a dangling edge e {v_1, s} incident to v_1
            p_dash = Update(p, Node.nodes.get(name=s))
            r_dash, d_dash = p_dash
            if not d_dash:
                return True
            p_dash_hash = P(r=frozenset(r_dash), d=frozenset(d_dash))
            if (bandwidthKplausible(p_dash, k)
                and T[p_dash_hash] == False):
                T[p_dash_hash] = True
                Q.append(p_dash)
        else:
            V = Unassigned(r, d)
            for s in V:
                p_dash = Update(p, Node.nodes.get(name=s))
                (r_dash, d_dash) = p_dash
                if not d_dash:
                     return True
                p_dash_hash = P(r=frozenset(r_dash), d=frozenset(d_dash))
                if (bandwidthKplausible(p_dash, k) and
                    T[p_dash_hash] == False):
                    T[p_dash_hash] = True
                    Q.append(p_dash)
    #print("Done!")
    return False
