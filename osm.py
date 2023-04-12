import os
os.environ['USE_PYGEOS'] = '0'
import osmnx as ox
import networkx as nx
import fiona
import shapely.geometry as geom
import geopandas as gpd
import traceback
from data_utils import create_folder

def load_osm_network():

    # Define the location and the network type
    place_name = "Lyon, France"
    network_type = "drive"

    # Retrieve the street network graph
    G = ox.graph_from_place(place_name, network_type=network_type, simplify=False)

    G = ox.project_graph(G, to_crs="EPSG:4171")

    # Save the graph data as a GeoPackage file
    create_folder("./data/osm")
    ox.save_graph_geopackage(G, filepath="./data/osm/lyon_drive.gpkg")

#load_osm_network()

def manhattan_distance(node1, node2):
    print(node1, node2)
    x1, y1 = node1
    x2, y2 = node2
    return abs(x1-x2) + abs(y1-y2)

def shortest_path(graph_file_path, shortest_path_file_path, origin_point, destination_point):
    # Load the graph data from the GeoPackage file

    gdf_edges = gpd.read_file(graph_file_path, layer='edges')
    gdf_nodes = gpd.read_file(graph_file_path, layer="nodes")

    gdf_edges = gdf_edges.set_index(['u', 'v', 'key'])
    gdf_nodes = gdf_nodes.set_index(['osmid'])

    G = ox.graph_from_gdfs(gdf_nodes, gdf_edges)

    G = ox.simplify_graph(G)

    # Choose two nodes in the graph to find the shortest path between
    # print(origin_point[1], origin_point[0])

    origin_node = ox.nearest_nodes(G, X=origin_point[1], Y=origin_point[0])
    destination_node = ox.nearest_nodes(G, X=destination_point[1], Y=destination_point[0])

    # print(origin_node)
    # print(destination_node)

    try:
        # Calculate the shortest path using Dijkstra's algorithm
        shortest_path = nx.astar_path(G, origin_node, destination_node, heuristic=manhattan_distance, weight="length")

        # Convert the shortest path to a LineString geometry
        route_edges = ox.utils_graph.get_route_edge_attributes(G, shortest_path)
        
        gdf_route_edges = gpd.GeoDataFrame(route_edges, crs=G.graph['crs'], geometry='geometry')

        gdf_route_edges.to_file(shortest_path_file_path, driver='GPKG')

        print("Shortest path found")

    except nx.NetworkXNoPath:
        traceback.print_exc()
        print("No path found")

#create_folder("./data/osm/shortest_path/")

origin_point = (45.7587374, 4.8459845)
destination_point = (45.7588047,4.846815)

shortest_path("./data/osm/lyon_drive.gpkg", "./data/osm/shortest_path/first_trial.gpkg", origin_point=origin_point, destination_point=destination_point)