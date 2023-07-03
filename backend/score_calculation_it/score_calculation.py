import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
import random
import pandas as pd
import multiprocessing as mp
import numpy as np
from shapely.wkt import loads, dumps
import os
import time
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import osmnx as ox
import math

from data_utils import *

###### NETWORK SCORE CALCULATION #######
create_folder("./output_data/network/graph/")

### GLOBAL VARIABLES ###
edges_buffer_path = "./input_data/network/edges_buffered_12_bounding.gpkg"
edges_buffer_arbres_prop_path = "./output_data/network/edges/edges_buffered_arbres_prop_bounding.gpkg"
edges_buffer_arbustes_prop_path = "./output_data/network/edges/edges_buffered_arbustes_prop_bounding.gpkg"
edges_buffer_prairies_prop_path = "./output_data/network/edges/edges_buffered_prairies_prop_bounding.gpkg"

edges_buffer_parcs_prop_path = "./output_data/network/edges/edges_buffered_parcs_prop_canop_bounding.gpkg"
edges_buffer_temp_wavg_path = "./output_data/network/edges/edges_buffered_temp_wavg_bounding.gpkg"
edges_buffer_eaux_prop_path = "./output_data/network/edges/edges_buffered_eaux_prop_bounding.gpkg"
edges_buffer_toilettes_path = "./output_data/network/edges/edges_buffered_toilette.gpkg"
edges_buffer_fontaines_potables_path = "./output_data/network/edges/edges_buffered_fontaines_potables.gpkg"
edges_buffer_fontaines_ornementales_path = "./output_data/network/edges/edges_buffered_fontaines_ornementales.gpkg"
edges_buffer_bancs_path = "./output_data/network/edges/edges_buffered_bancs.gpkg"

edges_buffer_scored_path = "./output_data/network/edges/edges_buffered_scored_bounding.gpkg"

# edges_buffer_scored_bounding_path = "./output_data/network/edges/edges_buffered_scored_bounding.gpkg"

edges_buffer_total_score_path = "./output_data/network/edges/edges_buffered_total_score_bounding.gpkg"
edges_buffer_total_score_distance_path = "./output_data/network/edges/edges_buffered_total_score_distance_bounding.gpkg"
edges_buffer_total_score_distance_freshness_path = "./output_data/network/edges/edges_buffered_total_score_distance_freshness_bounding.gpkg"

metrop_network_path = "./input_data/network/metrop_network_bounding.gpkg"
# metrop_network_bounding_path = "./output_data/network/graph/metrop_network_bounding.gpkg"
final_network_path = "./output_data/network/graph/final_network_bounding_no_poi_15.gpkg"

# bouding_mask_path = "./input_data/bounding_metrop.gpkg"

params = {
    "prairies_prop" : {
        "edges_path": edges_buffer_prairies_prop_path,
        "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
        "fn_cont": lambda x: -3*x+3
        },
    "arbustes_prop": {
        "edges_path": edges_buffer_arbustes_prop_path,
        "fn": lambda x: 1 if x>=0.4 else(3 if x>=0.2 and x<0.4 else 5),
        "fn_cont": lambda x: -5*x+5
        },
    "arbres_prop": {
        "edges_path": edges_buffer_arbres_prop_path,
        "fn": lambda x: 1 if x>=0.6 else(5 if x>=0.2 and x<0.6 else 20),
        "fn_cont": lambda x: -20*x+20
        },
    "C_wavg": {
        "edges_path": edges_buffer_temp_wavg_path,
        "fn": lambda x: 1 if x<33 else(5 if x>=33 and x<37 else 10),
        "fn_cont": lambda x: 1 if x<33 else(5 if x>=33 and x<37 else 10)
        },
    "eaux_prop": {
        "edges_path": edges_buffer_eaux_prop_path,
        "fn": lambda x: 1 if x > 0.7 else(3 if x >= 0.3 and x <=0.7 else 7),
        "fn_cont": lambda x: -7*x+7
        },
    "canop": {
        "edges_path": edges_buffer_parcs_prop_path,
        "fn": lambda x: 1 if x=="high" else(8 if x =="medium" else 15),
        "fn_cont": lambda x: -5*x+5
        },
    # "toilettes" :{
    #     "edges_path": edges_buffer_toilettes_path,
    #     "fn": lambda x: 1 if x==True else 4,
    #     "fn_cont": lambda x: 1 if x==True else 4
    # },
    # "fontaines_potables": {
    #     "edges_path": edges_buffer_fontaines_potables_path,
    #     "fn": lambda x: 1 if x==True else 5,
    #     "fn_cont": lambda x: 1 if x==True else 5
    # },
    # "fontaines_ornementales": {
    #     "edges_path": edges_buffer_fontaines_ornementales_path,
    #     "fn": lambda x: 1 if x==True else 3,
    #     "fn_cont": lambda x: 1 if x==True else 3
    # },
    # "bancs": {
    #     "edges_path": edges_buffer_bancs_path,
    #     "fn": lambda x: 1 if x==True else 1
    # }
}

### FUNCTIONS ###

def merge_networks(network1_path, network2_path, columns, output_path):
    """merge two networks with the list of columns of the second network to merge into the first"""
    network1 = gpd.read_file(network1_path)
    network2 = gpd.read_file(network2_path)

    network1 = network1.set_index(["u", "v", "key"])
    network2 = network2.set_index(["u", "v", "key"])

    network1.update(network2[columns])

    network1.to_file(output_path, driver="GPKG")
    
def total_score(input_path, output_path, score_columns):
    edges = gpd.read_file(input_path)
    edges["total_score"] = edges[score_columns].sum(axis=1)
    min_score = edges["total_score"].min()
    edges["total_score"] = edges.apply(lambda x: min_score if(x["score_canop"] < 2.5) else x["total_score"], axis=1)
    
    min_score = edges["total_score"].min()
    max_score = edges["total_score"].max()

    normalize_score = edges["total_score"].apply(lambda x: (x-min_score)/(max_score-min_score))

    edges["exp_score_15"] = normalize_score.apply(lambda x: (np.exp(x**1.5)-math.exp(0))/(math.exp(1)-math.exp(0)))
    edges["exp_score"] = normalize_score.apply(lambda x: (np.exp(x**3)-math.exp(0))/(math.exp(1)-math.exp(0)))

    edges.to_file(output_path, driver="GPKG")

def score_edges(input_path, output_path, params):
    """
    params : {
        columns1 : {
            edges_path: "path",
            fn: function()
            },
        },
        ...
    }
    """
    default_edges = gpd.read_file(input_path, layer="edges")

    score_columns = []
    
    for data_name, data_param in params.items():
        print(f"Score {data_name}")
        data = gpd.read_file(data_param["edges_path"])
        default_edges[f"score_{data_name}"] = data[data_name].apply(data_param["fn_cont"])
        score_columns.append(f"score_{data_name}")

    default_edges.to_file(output_path, driver="GPKG")

    return score_columns

def clip_bouding_data(data_path, mask_path, output_path):
    data = gpd.read_file(data_path)
    mask = gpd.read_file(mask_path)

    clipped_data = gpd.clip(data, mask)

    clipped_data.to_file(output_path)

def clip_bouding_graph(graph_path, mask_path, output_path):
    edges = gpd.read_file(graph_path, layer="edges")
    nodes = gpd.read_file(graph_path, layer="nodes")

    edges = edges.set_index(["u", "v", "key"])
    nodes = nodes.set_index(["osmid"])

    nodes["x"] = nodes["lon"]
    nodes["y"] = nodes["lat"]

    mask = gpd.read_file(mask_path)

    clipped_edges = gpd.clip(edges, mask, keep_geom_type=True)
    clipped_nodes = gpd.clip(nodes, mask, keep_geom_type=True)

    print("edges columns : ", clipped_edges.columns)
    print("nodes columns: ", clipped_nodes.columns)

    clipped_nodes.loc[:,"x"] = clipped_nodes["lon"]
    clipped_nodes.loc[:,"y"] = clipped_nodes["lat"]

    graph_attrs = {'crs': 'epsg:3946', 'simplified': True}

    G = ox.graph_from_gdfs(clipped_nodes, clipped_edges, graph_attrs)

    ox.save_graph_geopackage(G, output_path)

def score_distance(input_path, output_path, dist_prop, fresh_prop):
    """"""
    edges = gpd.read_file(input_path)
    # Standardize the length column
    # scaler = StandardScaler()
    # edges["length_standardized"] = scaler.fit_transform(edges[["length"]])

    # Scale the standardized length between 0 and 1
    min_max_scaler_dist = MinMaxScaler(feature_range=(0, 1))
    edges["length_scaled"] = min_max_scaler_dist.fit_transform(edges[["length"]])

    min_max_scaler_fresh = MinMaxScaler(feature_range=(0,1))
    edges["score_scaled"] = min_max_scaler_fresh.fit_transform(edges[["total_score"]])

    edges["score_distance_scaled"] = round(edges["total_score"] * edges["length_scaled"], 2)
    edges["score_distance"] = round(edges["total_score"] * edges["length"])

    edges["score_distance_prop"] = round(edges["score_scaled"]*fresh_prop+edges["length_scaled"]*dist_prop, 2)

    edges["score_sqrt"] = round(edges["total_score"]*(edges["length"]**0.5), 2)

    edges["score_sqrt_0604"] = round((edges["total_score"]**0.6)*(edges["length"]**0.4), 2)

    edges["exp_distance"] = round(edges["exp_score"]*edges["length"], 2)

    edges.to_file(output_path, driver="GPKG")

def score_fraicheur(input_path, output_path):
    """Score from 0 to 10 in term of freshness instead of heat"""
    edges = gpd.read_file(input_path)
    min_score = edges["total_score"].min()
    max_score = edges["total_score"].max()

    slope = (0-10)/(max_score-min_score)

    origin_ordinate = -slope*max_score

    print("pente : ", slope)
    print("origin_ordinate: ", origin_ordinate)

    edges["freshness_score"] = edges["total_score"].apply(lambda x: round(slope*x+origin_ordinate, 2))

    edges["exp_fresh_score"] = edges["exp_score"].apply(lambda x: -10*x+10)

    edges["exp_fresh_score_15"] = edges["exp_score_15"].apply(lambda x: -10*x+10)

    edges.to_file(output_path, driver="GPKG")

def create_graph(graph_path, edges_buffered_path, graph_output_path):
    graph_e = gpd.read_file(graph_path, layer="edges")
    graph_n = gpd.read_file(graph_path, layer="nodes")
    edges_buffered = gpd.read_file(edges_buffered_path)

    graph_e = graph_e.set_index(["u", "v", "key"])
    edges_buffered = edges_buffered.set_index(["u", "v", "key"])
    graph_n = graph_n.set_index(["osmid"])

    graph_e["total_score"] = edges_buffered["total_score"]
    graph_e["score_distance"] = edges_buffered["score_distance"]
    graph_e["score_distance_scaled"] = edges_buffered["score_distance_scaled"]
    graph_e["freshness_score"] = edges_buffered["freshness_score"]
    graph_e["score_distance_prop"] = edges_buffered["score_distance_prop"]
    graph_e["score_sqrt"] = edges_buffered["score_sqrt"]
    graph_e["score_sqrt_0604"] = edges_buffered["score_sqrt_0604"]

    graph_e["exp_distance"] = edges_buffered["exp_distance"]
    graph_e["exp_score"] = edges_buffered["exp_score"]
    graph_e["exp_fresh_score"] = edges_buffered["exp_fresh_score"]

    graph_e["exp_fresh_score_15"] = edges_buffered["exp_fresh_score_15"]

    G = ox.graph_from_gdfs(graph_n, graph_e)

    ox.save_graph_geopackage(G, graph_output_path)


s = time.time()

# score_columns = score_edges(edges_buffer_path, edges_buffer_scored_path, params)
score_columns = ["score_prairies_prop", "score_arbustes_prop", "score_arbres_prop", "score_C_wavg", "score_eaux_prop", "score_canop"]

# clip_bouding_data(edges_buffer_scored_path, bouding_mask_path, edges_buffer_scored_bounding_path)

total_score(edges_buffer_scored_path, edges_buffer_total_score_path, score_columns)
score_distance(edges_buffer_total_score_path, edges_buffer_total_score_distance_path,0.5,0.5)
score_fraicheur(edges_buffer_total_score_distance_path, edges_buffer_total_score_distance_freshness_path)

# clip_bouding_graph(metrop_network_path, bouding_mask_path, metrop_network_bounding_path)

create_graph(metrop_network_path, edges_buffer_total_score_distance_freshness_path, final_network_path)

# create_csv_dataset(final_network_path, "./output_data/csv/final_score_distance_edges_veget_temp.csv", "edges")

e = time.time()
duration = (e-s)/60
print("duration : ", duration)