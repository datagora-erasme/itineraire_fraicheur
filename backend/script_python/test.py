# Fichier de test : remove pour la prod

# tests sur la standardization des valeurs de fraîcheurs pour le network

import os
os.environ['USE_PYGEOS'] = '0'
import osmnx as ox
import networkx as nx
import fiona
import shapely.geometry as geom
import geopandas as gpd
import traceback
from data_utils import create_folder
import warnings
import numpy as np
import pandas as pd

data_folder_path = "./backend/data/osm/lyon_walk_simplified.gpkg"

default_ntf = "./backend/data/osm/lyon_walk_simplified.gpkg"

weighted_ntf = "./backend/data/osm/joined_temp_road_veget.gpkg"

cf = "./backend/script_python/data/raw_data/joined_if_3946.gpkg"

op = "./backend/data/osm/test_sd.gpkg"

g = "./backend/data/osm/test_weighted.gpkg"



default_edges = gpd.read_file(default_ntf, layer="edges")

weighted_edges = gpd.read_file(weighted_ntf)

default_nodes = gpd.read_file(default_ntf, layer="nodes")

# print("default_edges.size : ", default_edges.size)
# print("weighted_edges.size : ", weighted_edges.size)

# For some reason pandas convert u, v and key into float for weighted_edges
weighted_edges[["u", "v", "key"]] = weighted_edges[["u", "v", "key"]].astype(int)

# print(default_edges.head())

# print(weighted_edges.head())

# grouped_edges = weighted_edges.groupby(["u", "v", "key"]).apply(lambda x: np.multiply(x["IF"], x["length"])/np.sum(x["length"]))


# grouped_edges = weighted_edges.groupby(["u", "v", "key"]).apply(lambda x: np.average(x["IF"], weights=x["length"])).reset_index()

grouped_edges = weighted_edges.groupby(["u", "v", "key"]).apply(lambda x: pd.Series({
    "weighted_IF": np.average(x["IF"], weights=x["length"])
})).reset_index()


print(grouped_edges.head())


print(grouped_edges.value_counts())

print("default : ", len(default_edges))
print("weighted : ", len(weighted_edges))
print("grouped : ", len(grouped_edges))

grouped_edges = grouped_edges.set_index(["u", "v", "key"])
default_edges = default_edges.set_index(["u", "v", "key"])

default_edges["weighted_IF"] = grouped_edges["weighted_IF"]

print(default_edges.head())

default_nodes = default_nodes.set_index(['osmid'])

G = ox.graph_from_gdfs(default_nodes, default_edges)

ox.save_graph_geopackage(G, filepath=g)


def merge_network_data(network_file, data_file, output_file):
    """Use an osm network and merge data gpkd polygon file"""
    print("loading network and data file")
    edges = gpd.read_file(network_file, layer="edges")
    nodes = gpd.read_file(network_file, layer="nodes")
    data = gpd.read_file(data_file)

    print("original edges : ", type(edges))
    print(edges.head())
    print("length: \n", edges.length)

    data_reprojected = data.to_crs(edges.crs)

    print("calculating intersection between edges and data")
    intersections = gpd.overlay(edges, data_reprojected, how="intersection")
    print(intersections.head())

    print(intersections.length)

    print("recalculating length of intersections")
    intersections['length'] = intersections.geometry.length
    print(intersections.length)

    print("calculating standardized freshness for each edge")
    edge_data = intersections.groupby(['u', 'v', 'key'])\
        .apply(lambda x: np.average(x['IF'], weights=x['length']))\
        .reset_index(name='sd_IF')

    edge_data = edge_data.set_index(['u', 'v', 'key'])

    print("calculated edges : ", type(edge_data))
    print(edge_data.head())
    print("length: \n", edge_data.size)

    # nodes = nodes.set_index(['osmid'])

    # G = ox.graph_from_gdfs(nodes, edge_data)

    # ox.save_graph_geopackage(G, filepath=output_file)
    print("done")

# merge_network_data(ntf, cf, op)