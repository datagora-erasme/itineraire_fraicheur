import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
import random
import pandas as pd
import multiprocessing as mp
import numpy as np
import osmnx as ox
import json
import networkx as nx
import pickle
from data_utils import *

import plotly.express as px
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

## FUNCTION : 
def load_graph_from_pickle(pickle_path):
    # Load the graph from the pickle file
    with open(pickle_path, 'rb') as f:
        G = pickle.load(f)

    return G

def shortest_path(G, start, end, G_multidigraph, index, global_gdf):
    origin_node = ox.nearest_nodes(G, X=start[0], Y=start[1])
    destination_node = ox.nearest_nodes(G, X=end[0], Y=end[1])

    print("Finding shortest path IF ...")

    shortest_path_if = nx.shortest_path(G, source=origin_node, target=destination_node, weight="score_distance") #IF_LENGTH_7030

    # print("shortest_path_if:", shortest_path_if)

    route_edges_if = ox.utils_graph.route_to_gdf(G_multidigraph, shortest_path_if)

    # print("route_edges_if: ", route_edges_if)

    gdf_route_edges_if = gpd.GeoDataFrame(route_edges_if, crs=G.graph['crs'], geometry='geometry')

    gdf_route_edges_if = gdf_route_edges_if.to_crs(epsg=4326)

    gdf_route_edges_if["type"] = "IF"
    gdf_route_edges_if["id_it"] = index

    gdf_route_edges_if = gdf_route_edges_if.reset_index()
    gdf_route_edges_if = gdf_route_edges_if.set_index(["u", "v", "key", "type", "id_it"])

    print("Finding shortest path Length ...")

    shortest_path_len = nx.shortest_path(G, source=origin_node, target=destination_node, weight="length")

    route_edges_len = ox.utils_graph.route_to_gdf(G_multidigraph, shortest_path_len)

    gdf_route_edges_len = gpd.GeoDataFrame(route_edges_len, crs=G.graph['crs'], geometry='geometry')

    gdf_route_edges_len = gdf_route_edges_len.to_crs(epsg=4326)

    gdf_route_edges_len["type"] = "LEN"
    gdf_route_edges_len["id_it"] = index

    gdf_route_edges_len = gdf_route_edges_len.reset_index()
    gdf_route_edges_len = gdf_route_edges_len.set_index(["u", "v", "key", "type", "id_it"])

    sum_distance = gdf_route_edges_len["length"].sum()

    if(sum_distance >= 200):
        global_gdf = pd.concat([global_gdf, gdf_route_edges_if])
        global_gdf = pd.concat([global_gdf, gdf_route_edges_len])

    return global_gdf

def clipp_graph_nodes_from_zone(zone_path, zone_id, graph_path, clipped_nodes_path):
    ## CLIP GRAPH NODES
    print("read zones file")
    studies_zones = gpd.read_file(zone_path)

    zone = studies_zones[studies_zones["zone_id"] == zone_id]
    zone = zone.to_crs(3946)

    print(zone)

    print("read graph file")

    graph_n = gpd.read_file(graph_path, layer="nodes")

    graph_n = graph_n.to_crs(3946)

    graph_n_zone = graph_n.overlay(zone, how="intersection")

    print("saving file")
    graph_n_zone.to_file(clipped_nodes_path, layer="nodes", driver="GPKG")
    print("ALL DONE")


def create_random_itineraries(nodes_path, graph_path, multidigraph_path, n_itineraries, itineraries_path):
    ## SELECT RANDOM POINTS
    nodes = gpd.read_file(nodes_path, layer="nodes").set_index(["osmid"])

    random_nodes = nodes.sample(n=n_itineraries)
    start_nodes = random_nodes[0:round((n_itineraries)/2)]
    end_nodes = random_nodes[100:n_itineraries]

    ## CREATE RANDOM ITINERARIES
    G = load_graph_from_pickle(graph_path)
    MG = load_graph_from_pickle(multidigraph_path)

    count = 0

    global_gdf = gpd.GeoDataFrame()

    for i in range(0,round(n_itineraries/2)):
        print(f"It {i} .. ")
        start = (start_nodes.iloc[i]["lon"], start_nodes.iloc[i]["lat"])
        end = (end_nodes.iloc[i]["lon"], end_nodes.iloc[i]["lat"])
        print(start, end)
        global_gdf = shortest_path(G, start, end, MG, count, global_gdf)
        count+=1

    print("saving file")
    global_gdf.to_file(itineraries_path, driver="GPKG", layer="itineraries")
    print("ALL DONE")


## GLOBAL VARIABLES
zones_path = "./input_data/studies_zones/studies_sectors.gpkg"
graph_path = "./output_data/network/graph/final_network_bounding_scaled_no_na.gpkg"
clipped_nodes_tetedor_path = "./output_data/studies_zones/tetedor_nodes.gpkg"
clipped_nodes_partdieu_path = "./output_data/studies_zones/partdieu/partdieu_nodes.gpkg"

graph_pickle = "./output_data/network/graph/final_network_bounding_scaled_no_na.pickle"
multidigraph_pickle = "./output_data/network/graph/final_network_bounding_scaled_no_na_multidigraph.pickle"

tetedor_itineraries_path = "./output_data/studies_zones/tetedor/100_it.gpkg"
partdieu_itineraries_path = "./output_data/studies_zones/partdieu/partdieu_100_it.gpkg"

## SCRIPT

### TETE D'OR

# clipp_graph_nodes_from_zone(zones_path, "tetedor", graph_path, clipped_nodes_tetedor_path)
# create_random_itineraries(clipped_nodes_tetedor_path, graph_pickle, multidigraph_pickle, 200, tetedor_itineraries_path)

## PART DIEU
clipp_graph_nodes_from_zone(zones_path, "partdieu", graph_path, clipped_nodes_partdieu_path)
create_random_itineraries(clipped_nodes_partdieu_path, graph_pickle, multidigraph_pickle, 200, partdieu_itineraries_path)