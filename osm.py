import os
os.environ['USE_PYGEOS'] = '0'
import osmnx as ox
import networkx as nx
import fiona
import shapely.geometry as geom
import geopandas as gpd
import traceback
from data_utils import create_folder


def load_osm_network(network_paramaters):
    print("Loading OSM network")

    # Retrieve the street network graph
    if(network_paramaters["bbox"] !=None):
        north, south, east, west = network_paramaters["bbox"]
        G = ox.graph_from_bbox(north, south, east, west, network_type=network_paramaters["network_type"], simplify=True)
    else:
        G = ox.graph_from_place(network_paramaters["place_name"], network_type=network_paramaters["network_type"], simplify=False)

    G = ox.project_graph(G, to_crs="EPSG:4171")

    print("OSM network loaded, saving into file..")
    # Save the graph data as a GeoPackage file
    create_folder("./data/osm")
    ox.save_graph_geopackage(G, filepath=network_paramaters["output_file"])

lyon_network_parameters = {
    "place_name" : "Lyon, France",
    "network_type" : "drive",
    "bbox": None,
    "output_file": "./data/osm/lyon_drive.gpkg"
}


bbox_network_parameters = {
    "place_name": "Lyon, France",
    "network_type": "walk",
    "bbox": (45.76091,45.74938, 4.89007,4.86426),
    "output_file" : "./data/osm/bbox_default_crs.gpkg"
}

# load_osm_network(lyon_network_parameters)
# load_osm_network(bbox_network_parameters)

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

    print(gdf_nodes.columns)
    print(gdf_nodes.index)

    print(gdf_nodes.loc[208769027])
    print(gdf_nodes.loc[208769047])
    G = ox.graph_from_gdfs(gdf_nodes, gdf_edges)

    origin_node = ox.nearest_nodes(G, X=origin_point[1], Y=origin_point[0])
    destination_node = ox.nearest_nodes(G, X=destination_point[1], Y=destination_point[0])

    print(origin_node)
    print(destination_node)

    print("type G : ", type(G))

    try:
        # Calculate the shortest path astar's algorithm
        #shortest_path = nx.astar_path(G, origin_node, destination_node, heuristic=manhattan_distance, weight="length")
        # Calculate the shortest path using Dijkstra's algorithm
        shortest_path = nx.shortest_path(G, source=origin_node, target=destination_node, weight="length")


        print(type(shortest_path))
        print(shortest_path)

        # Convert the shortest path to a LineString geometry
        route_edges = ox.utils_graph.get_route_edge_attributes(G, shortest_path)
        
        gdf_route_edges = gpd.GeoDataFrame(route_edges, crs=G.graph['crs'], geometry='geometry')

        gdf_route_edges.to_file(shortest_path_file_path, driver='GPKG')

        print("Shortest path found")

    except nx.NetworkXNoPath:
        traceback.print_exc()
        print("No path found")

#create_folder("./data/osm/shortest_path/")

origin_point = (45.7587161, 4.8737715)
destination_point = (45.7596251,4.8743205)

shortest_path("./data/osm/bbox_default_crs.gpkg", "./data/osm/shortest_path/_bbox_first_trial.gpkg", origin_point=origin_point, destination_point=destination_point)
