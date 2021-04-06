#
#  Node.py
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



from neomodel import StructuredNode 
from neomodel import StringProperty 
from neomodel import IntegerProperty
from neomodel import FloatProperty
from neomodel import RelationshipTo
from neomodel import RelationshipFrom
from neomodel import config

class Node(StructuredNode):
    name = StringProperty(unique_index=True, required=True)
    operand_1 = FloatProperty(required=True)
    operand_2 = FloatProperty(required=True)
    result = FloatProperty(required=True)
    operator = StringProperty(required=True)
    directed_edges = RelationshipTo('Node', 'CONNECTED')