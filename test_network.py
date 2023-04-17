# import os
# os.environ['USE_PYGEOS'] = '0'
from pyrosm import OSM, get_data
import osmnx as ox

# Initialize the reader
osm = OSM(get_data("lyon"))

# Get all walkable roads and the nodes 
nodes, edges = osm.get_network(nodes=True)

# Check first rows in the edge 
edges.head()

# Create NetworkX graph
G = osm.to_graph(nodes, edges, graph_type="networkx")

# source_address = "240 avenue Félix Faure, Lyon"
# target_address = "4 rue audibert et lavirotte, Lyon"

# source = ox.geocode(source_address)
# target = ox.geocode(target_address)

source = (4.8725638, 45.7583679)
target = (4.8743205, 45.7596251)

# Source and target are now points tuple of (x, y) coordinates
print(source)
print(target)
sx,sy = source
tx, ty = source

# Find the closest nodes from the graph
source_node = ox.nearest_nodes(G, sx, sy)
target_node = ox.nearest_nodes(G, tx, ty)

# Check the nodeids of the source/target node
print(source_node)
print(target_node)

# Find shortest path (by distance)
import networkx as nx
route = nx.shortest_path(G, source_node, target_node, weight="length")
print(route)
