import osmnx as ox
from data_utils import create_folder

# Define the location and the network type
place_name = "Lyon, France"
network_type = "drive"

# Retrieve the street network graph
G = ox.graph_from_place(place_name, network_type=network_type)

# Save the graph data as a GeoPackage file
create_folder("./data/osm")
ox.save_graph_geopackage(G, filepath="./data/osm/lyon_drive.gpkg")