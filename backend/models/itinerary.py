import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
import networkx as nx
import osmnx as ox
import pickle
import time
import json

def load_graph_from_pickle(pickle_path):
    # Load the graph from the pickle file
    with open(pickle_path, 'rb') as f:
        G = pickle.load(f)

    return G

def shortest_path(G, start, end, G_multidigraph):
    origin_node = ox.nearest_nodes(G, X=start[0], Y=start[1])
    destination_node = ox.nearest_nodes(G, X=end[0], Y=end[1])

    print("Finding shortest path IF ...")

    shortest_path_if = nx.shortest_path(G, source=origin_node, target=destination_node, weight="score_distance") #IF_LENGTH_7030

    route_edges_if = ox.utils_graph.get_route_edge_attributes(G_multidigraph, shortest_path_if)

    gdf_route_edges_if = gpd.GeoDataFrame(route_edges_if, crs=G.graph['crs'], geometry='geometry')

    gdf_route_edges_if = gdf_route_edges_if.to_crs(epsg=4326)

    geojson_if = json.loads(gdf_route_edges_if.to_json())

    gdf_route_edges_if.to_file("./temp/if_test_2806_ts.json", driver="GeoJSON")

    print("Finding shortest path Length ...")

    shortest_path_len = nx.shortest_path(G, source=origin_node, target=destination_node, weight="length")

    route_edges_len = ox.utils_graph.get_route_edge_attributes(G_multidigraph, shortest_path_len)

    gdf_route_edges_len = gpd.GeoDataFrame(route_edges_len, crs=G.graph['crs'], geometry='geometry')

    gdf_route_edges_len = gdf_route_edges_len.to_crs(epsg=4326)

    geojson_len = json.loads(gdf_route_edges_len.to_json())

    gdf_route_edges_len.to_file("./temp/len_test_2806_ts.json", driver="GeoJSON")

    return geojson_if, geojson_len

# global :  5.0173704624176025
# node:  1.904900312423706
# sp :  0.004061222076416016
# convert :  3.104257345199585
# multidigraph :  3.097426652908325
# route_edges :  8.368492126464844e-05
# gpd :  0.0014109611511230469
# geojson :  0.004133939743041992