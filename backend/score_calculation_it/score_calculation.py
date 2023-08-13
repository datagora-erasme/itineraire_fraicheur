#%%
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

#%%
###### NETWORK SCORE CALCULATION #######
create_folder("./output_data/network/graph/")

### GLOBAL VARIABLES ###
edges_buffer_path = "./input_data/network/edges_buffered_12_bounding.gpkg"
edges_buffer_arbres_prop_path = "./output_data/network/edges/edges_buffered_arbres_prop_bounding.gpkg"
edges_buffer_arbustes_prop_path = "./output_data/network/edges/edges_buffered_arbustes_prop_bounding.gpkg"
edges_buffer_prairies_prop_path = "./output_data/network/edges/edges_buffered_prairies_prop_bounding.gpkg"

edges_buffer_ombres_08_prop_path = "./output_data/network/edges/edges_buffered_ombres_08_prop_bounding.gpkg"
edges_buffer_ombres_13_prop_path = "./output_data/network/edges/edges_buffered_ombres_13_prop_bounding.gpkg"
edges_buffer_ombres_18_prop_path = "./output_data/network/edges/edges_buffered_ombres_18_prop_bounding.gpkg"

edges_buffer_parcs_prop_path = "./output_data/network/edges/edges_buffered_parcs_prop_canop_bounding.gpkg"
edges_buffer_temp_wavg_path = "./output_data/network/edges/edges_buffered_temp_wavg_bounding_no_na.gpkg"
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
final_network_path = "./output_data/network/graph/final_network_P1O8At2Ar10C6E7Ca8.gpkg"

# bouding_mask_path = "./input_data/bounding_metrop.gpkg"

score_columns = ["score_prairies_prop", "score_arbustes_prop", "score_arbres_prop", "score_C_wavg_scaled", "score_eaux_prop", "score_canop"]

params = {
    "prairies_prop" : {
        "edges_path": edges_buffer_prairies_prop_path,
        # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
        "fn_cont": lambda x: 1*(1-x),
        "alpha": 1
        },
    "ombres_08_prop" : {
        "edges_path": edges_buffer_ombres_08_prop_path,
        # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
        "fn_cont": lambda x: 8*(1-x),
        "alpha": 8
        },
    "ombres_13_prop" : {
        "edges_path": edges_buffer_ombres_13_prop_path,
        # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
        "fn_cont": lambda x: 8*(1-x),
        "alpha": 8
        },
    "ombres_18_prop" : {
        "edges_path": edges_buffer_ombres_18_prop_path,
        # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
        "fn_cont": lambda x: 8*(1-x),
        "alpha": 8
        },
    "arbustes_prop": {
        "edges_path": edges_buffer_arbustes_prop_path,
        # "fn": lambda x: 1 if x>=0.4 else(3 if x>=0.2 and x<0.4 else 5),
        "fn_cont": lambda x: 2*(1-x),
        "alpha": 2
        },
    "arbres_prop": {
        "edges_path": edges_buffer_arbres_prop_path,
        # "fn": lambda x: 1 if x>=0.6 else(5 if x>=0.2 and x<0.6 else 20),
        "fn_cont": lambda x: 10*(1-x),
        "alpha": 10
        },
    "C_wavg_scaled": {
        "edges_path": edges_buffer_temp_wavg_path,
        # "fn": lambda x: 1 if x<33 else(5 if x>=33 and x<37 else 10),
        "fn_cont": lambda x: 6*(1-x),
        "alpha": 6
        },
    "eaux_prop": {
        "edges_path": edges_buffer_eaux_prop_path,
        # "fn": lambda x: 1 if x > 0.7 else(3 if x >= 0.3 and x <=0.7 else 7),
        "fn_cont": lambda x: 7*(1-x),
        "alpha": 7
        },
    "canop": {
        "edges_path": edges_buffer_parcs_prop_path,
        # "fn": lambda x: 1 if x=="high" else(8 if x =="medium" else 15),
        "fn_cont": lambda x: 8*(1-x),
        "alpha": 8
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

def create_uniqID(x):
    """OSMNX invert some u and v when creating graph => create uniqId in order to make the analyse"""
    return str(x["u"])+str(x["v"])+str(x["key"])

def all_prop(input_path, params, output_path):
    """create one file with all props"""
    edges = gpd.read_file(input_path, layer="edges")
    edges["uniqId"] = edges.apply(create_uniqID, axis=1)
    edges = edges.set_index(["u", "v", "key"])
    for dataname, dataprops in params.items():
        data = gpd.read_file(dataprops["edges_path"])
        data = data.set_index(["u", "v", "key"])
        edges[dataname] = data[dataname]
    edges.to_file(output_path, layer="edges", driver="GPKG")
    
def total_score(input_path, output_path, score_columns):
    edges = gpd.read_file(input_path, layer="edges")
    print(edges.columns)
    edges["total_score"] = edges[score_columns].sum(axis=1)
    edges["total_score_08"] = edges["total_score"] + edges["score_ombres_08_prop"]
    edges["total_score_13"] = edges["total_score"] + edges["score_ombres_13_prop"]
    edges["total_score_18"] = edges["total_score"] + edges["score_ombres_18_prop"]

    # min_score = edges["total_score"].min()
    # # edges["total_score"] = edges.apply(lambda x: min_score if(x["score_canop"] < 0.05) else x["total_score"], axis=1)
    
    # min_score = edges["total_score"].min()
    # max_score = edges["total_score"].max()

    # print("min_score: ", min_score)
    # print("max_score: ", max_score)

    # normalize_score = edges["total_score"].apply(lambda x: (x-min_score)/(max_score-min_score))

    # edges["exp_score_15"] = normalize_score.apply(lambda x: (np.exp(x**1.5)-math.exp(0))/(math.exp(1)-math.exp(0)))
    # edges["exp_score"] = normalize_score.apply(lambda x: (np.exp(x**3)-math.exp(0))/(math.exp(1)-math.exp(0)))

    edges.to_file(output_path, driver="GPKG")

def all_score_edges(input_path, output_path, params):
    """
    params : {
        columns1 : {
            edges_path: "path",
            fn_cont: function(),
            alpha: 1
            },
        },
        ...
    }
    """
    default_edges = gpd.read_file(input_path, layer="edges")
    
    for data_name, data_param in params.items():
        print(f"Score {data_name}")
        data = gpd.read_file(data_param["edges_path"])
        default_edges[f"score_{data_name}"] = data[data_name].apply(data_param["fn_cont"])

    default_edges.to_file(output_path, driver="GPKG", layer="edges")

def one_score_edges(input_path, output_path, params, key):
    """(Re)-calculate score for one data"""
    default_edges = gpd.read_file(input_path, layer="edges")
    data = gpd.read_file(params[key]["edges_path"])
    default_edges[f"score_{key}"] = data[key].apply(params[key]["fn_cont"])

    default_edges.to_file(output_path, driver="GPKG")

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
    # min_max_scaler_dist = MinMaxScaler(feature_range=(0, 1))
    # edges["length_scaled"] = min_max_scaler_dist.fit_transform(edges[["length"]])

    # min_max_scaler_fresh = MinMaxScaler(feature_range=(0,1))
    # edges["score_scaled"] = min_max_scaler_fresh.fit_transform(edges[["total_score"]])

    # edges["score_distance_scaled"] = round(edges["total_score"] * edges["length_scaled"], 2)

    edges["score_distance_08"] = round(edges["total_score_08"] * edges["length"])
    edges["score_distance_13"] = round(edges["total_score_13"] * edges["length"])
    edges["score_distance_18"] = round(edges["total_score_18"] * edges["length"])

    # edges["score_distance_prop"] = round(edges["score_scaled"]*fresh_prop+edges["length_scaled"]*dist_prop, 2)

    # edges["score_sqrt"] = round(edges["total_score"]*(edges["length"]**0.5), 2)

    # edges["score_sqrt_0604"] = round((edges["total_score"]**0.6)*(edges["length"]**0.4), 2)

    # edges["exp_distance"] = round(edges["exp_score"]*edges["length"], 2)

    edges.to_file(output_path, driver="GPKG")

def score_fraicheur(input_path, output_path):
    """Score from 0 to 10 in term of freshness instead of heat"""
    edges = gpd.read_file(input_path)
    min_score = edges["total_score"].min()
    max_score = edges["total_score"].max()

    slope = (0-10)/(max_score-min_score)

    origin_ordinate = -slope*max_score

    # print("pente : ", slope)
    # print("origin_ordinate: ", origin_ordinate)

    edges["freshness_score"] = edges["total_score"].apply(lambda x: round(slope*x+origin_ordinate, 2))

    # edges["exp_fresh_score"] = edges["exp_score"].apply(lambda x: -10*x+10)

    # edges["exp_fresh_score_15"] = edges["exp_score_15"].apply(lambda x: -10*x+10)

    edges.to_file(output_path, driver="GPKG")

def create_graph(graph_path, edges_buffered_path, graph_output_path):
    graph_e = gpd.read_file(graph_path, layer="edges")
    graph_n = gpd.read_file(graph_path, layer="nodes")
    edges_buffered = gpd.read_file(edges_buffered_path)

    graph_e["uniqId"] = graph_e.apply(create_uniqID, axis=1)

    graph_e = graph_e.set_index(["u", "v", "key"])
    edges_buffered = edges_buffered.set_index(["u", "v", "key"])
    graph_n = graph_n.set_index(["osmid"])

    print(graph_e["uniqId"])

    print("ok")

    graph_e["total_score_08"] = edges_buffered["total_score_08"]
    graph_e["total_score_13"] = edges_buffered["total_score_13"]
    graph_e["total_score_18"] = edges_buffered["total_score_18"]
    graph_e["score_distance_08"] = edges_buffered["score_distance_08"]
    graph_e["score_distance_13"] = edges_buffered["score_distance_13"]
    graph_e["score_distance_18"] = edges_buffered["score_distance_18"]
    # graph_e["score_distance_scaled"] = edges_buffered["score_distance_scaled"]
    graph_e["freshness_score"] = edges_buffered["freshness_score"]
    # graph_e["score_distance_prop"] = edges_buffered["score_distance_prop"]
    # graph_e["score_sqrt"] = edges_buffered["score_sqrt"]
    # graph_e["score_sqrt_0604"] = edges_buffered["score_sqrt_0604"]

    # graph_e["exp_distance"] = edges_buffered["exp_distance"]
    # graph_e["exp_score"] = edges_buffered["exp_score"]
    # graph_e["exp_fresh_score"] = edges_buffered["exp_fresh_score"]

    # graph_e["exp_fresh_score_15"] = edges_buffered["exp_fresh_score_15"]

    G = ox.graph_from_gdfs(graph_n, graph_e)

    ox.save_graph_geopackage(G, graph_output_path)

def score_calculation_pipeline(meta_params):

    for params_name, params in meta_params.items():
        print(f"Starting score calculation for {params_name}...")
        all_score_edges(edges_buffer_path, edges_buffer_scored_path, params["params"])
        total_score(edges_buffer_scored_path, edges_buffer_total_score_path, score_columns)
        score_distance(edges_buffer_total_score_path, edges_buffer_total_score_distance_path,0.5,0.5)
        score_fraicheur(edges_buffer_total_score_distance_path, edges_buffer_total_score_distance_freshness_path)
        create_graph(metrop_network_path, edges_buffer_total_score_distance_freshness_path, params["graph_path"])

        weights_path = "./weights_score.csv"

        # Check if the weights file is empty
        try:
            weights = pd.read_csv(weights_path)
        except pd.errors.EmptyDataError:
            # If the file is empty, create a new DataFrame with columns
            weights = pd.DataFrame(columns=["graph_file", "arbres", "ombres" "arbustes", "prairies", "temp", "canop", "eaux"])

        currents_weights = pd.DataFrame({
            "graph_file": params["graph_path"],
            "arbres": params["params"]["arbres_prop"]["alpha"],
            "ombres": params["params"]["ombres_08_prop"]["alpha"],
            "arbustes": params["params"]["arbustes_prop"]["alpha"],
            "prairies": params["params"]["prairies_prop"]["alpha"],
            "temp": params["params"]["C_wavg_scaled"]["alpha"],
            "canop": params["params"]["canop"]["alpha"],
            "eaux": params["params"]["eaux_prop"]["alpha"]
        }, index=[0])

        concat_weights = pd.concat([weights, currents_weights])

        concat_weights.to_csv(weights_path, index=False)

meta_params = {
    "P1O8At2Ar10C6E7Ca8" : {
        "graph_path": "./output_data/network/graph/final_network_P1O8At2Ar10C6E7Ca8.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 1*(1-x),
            "alpha": 1
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 8*(1-x),
            "alpha": 8
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 8*(1-x),
            "alpha": 8
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 8*(1-x),
            "alpha": 8
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            # "fn": lambda x: 1 if x>=0.4 else(3 if x>=0.2 and x<0.4 else 5),
            "fn_cont": lambda x: 2*(1-x),
            "alpha": 2
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(5 if x>=0.2 and x<0.6 else 20),
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            # "fn": lambda x: 1 if x<33 else(5 if x>=33 and x<37 else 10),
            "fn_cont": lambda x: 6*(1-x),
            "alpha": 6
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            # "fn": lambda x: 1 if x > 0.7 else(3 if x >= 0.3 and x <=0.7 else 7),
            "fn_cont": lambda x: 7*(1-x),
            "alpha": 7
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            # "fn": lambda x: 1 if x=="high" else(8 if x =="medium" else 15),
            "fn_cont": lambda x: 8*(1-x),
            "alpha": 8
            },
        },
    },
    "P1O1At1Ar10C1E1Ca1" : {
        "graph_path": "./output_data/network/graph/final_network_P1O1At1Ar10C1E1Ca1.gpkg",
        "params" : {
            "prairies_prop" : {
                "edges_path": edges_buffer_prairies_prop_path,
                # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
                "fn_cont": lambda x: 1*(1-x),
                "alpha": 1
                },
            "ombres_08_prop" : {
                "edges_path": edges_buffer_ombres_08_prop_path,
                # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
                "fn_cont": lambda x: 1*(1-x),
                "alpha": 1
                },
            "ombres_13_prop" : {
                "edges_path": edges_buffer_ombres_13_prop_path,
                # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
                "fn_cont": lambda x: 1*(1-x),
                "alpha": 1
                },
            "ombres_18_prop" : {
                "edges_path": edges_buffer_ombres_18_prop_path,
                # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
                "fn_cont": lambda x: 1*(1-x),
                "alpha": 1
                },
            "arbustes_prop": {
                "edges_path": edges_buffer_arbustes_prop_path,
                # "fn": lambda x: 1 if x>=0.4 else(3 if x>=0.2 and x<0.4 else 5),
                "fn_cont": lambda x: 1*(1-x),
                "alpha": 1
                },
            "arbres_prop": {
                "edges_path": edges_buffer_arbres_prop_path,
                # "fn": lambda x: 1 if x>=0.6 else(5 if x>=0.2 and x<0.6 else 20),
                "fn_cont": lambda x: 10*(1-x),
                "alpha": 10
                },
            "C_wavg_scaled": {
                "edges_path": edges_buffer_temp_wavg_path,
                # "fn": lambda x: 1 if x<33 else(5 if x>=33 and x<37 else 10),
                "fn_cont": lambda x: 1*(1-x),
                "alpha": 1
                },
            "eaux_prop": {
                "edges_path": edges_buffer_eaux_prop_path,
                # "fn": lambda x: 1 if x > 0.7 else(3 if x >= 0.3 and x <=0.7 else 7),
                "fn_cont": lambda x: 1*(1-x),
                "alpha": 1
                },
            "canop": {
                "edges_path": edges_buffer_parcs_prop_path,
                # "fn": lambda x: 1 if x=="high" else(8 if x =="medium" else 15),
                "fn_cont": lambda x: 1*(1-x),
                "alpha": 1
                },
        }
    },
    "P1O1At1Ar100C1E1Ca1" : {
        "graph_path": "./output_data/network/graph/final_network_P1O1At1Ar100C1E1Ca1.gpkg",
        "params" : {
            "prairies_prop" : {
                "edges_path": edges_buffer_prairies_prop_path,
                # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
                "fn_cont": lambda x: 1*(1-x),
                "alpha": 1
                },
            "ombres_08_prop" : {
                "edges_path": edges_buffer_ombres_08_prop_path,
                # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
                "fn_cont": lambda x: 1*(1-x),
                "alpha": 1
                },
            "ombres_13_prop" : {
                "edges_path": edges_buffer_ombres_13_prop_path,
                # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
                "fn_cont": lambda x: 1*(1-x),
                "alpha": 1
                },
            "ombres_18_prop" : {
                "edges_path": edges_buffer_ombres_18_prop_path,
                # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
                "fn_cont": lambda x: 1*(1-x),
                "alpha": 1
                },
            "arbustes_prop": {
                "edges_path": edges_buffer_arbustes_prop_path,
                # "fn": lambda x: 1 if x>=0.4 else(3 if x>=0.2 and x<0.4 else 5),
                "fn_cont": lambda x: 1*(1-x),
                "alpha": 1
                },
            "arbres_prop": {
                "edges_path": edges_buffer_arbres_prop_path,
                # "fn": lambda x: 1 if x>=0.6 else(5 if x>=0.2 and x<0.6 else 20),
                "fn_cont": lambda x: 100*(1-x),
                "alpha": 100
                },
            "C_wavg_scaled": {
                "edges_path": edges_buffer_temp_wavg_path,
                # "fn": lambda x: 1 if x<33 else(5 if x>=33 and x<37 else 10),
                "fn_cont": lambda x: 1*(1-x),
                "alpha": 1
                },
            "eaux_prop": {
                "edges_path": edges_buffer_eaux_prop_path,
                # "fn": lambda x: 1 if x > 0.7 else(3 if x >= 0.3 and x <=0.7 else 7),
                "fn_cont": lambda x: 1*(1-x),
                "alpha": 1
                },
            "canop": {
                "edges_path": edges_buffer_parcs_prop_path,
                # "fn": lambda x: 1 if x=="high" else(8 if x =="medium" else 15),
                "fn_cont": lambda x: 1*(1-x),
                "alpha": 1
                },
        }
    },
    "P1O8At1Ar10C1E1Ca1" : {
        "graph_path": "./output_data/network/graph/final_network_P1O8At1Ar10C1E1Ca1.gpkg",
        "params" : {
            "prairies_prop" : {
                "edges_path": edges_buffer_prairies_prop_path,
                # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
                "fn_cont": lambda x: 1*(1-x),
                "alpha": 1
                },
            "ombres_08_prop" : {
                "edges_path": edges_buffer_ombres_08_prop_path,
                # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
                "fn_cont": lambda x: 8*(1-x),
                "alpha": 8
                },
            "ombres_13_prop" : {
                "edges_path": edges_buffer_ombres_13_prop_path,
                # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
                "fn_cont": lambda x: 8*(1-x),
                "alpha": 8
                },
            "ombres_18_prop" : {
                "edges_path": edges_buffer_ombres_18_prop_path,
                # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
                "fn_cont": lambda x: 8*(1-x),
                "alpha": 8
                },
            "arbustes_prop": {
                "edges_path": edges_buffer_arbustes_prop_path,
                # "fn": lambda x: 1 if x>=0.4 else(3 if x>=0.2 and x<0.4 else 5),
                "fn_cont": lambda x: 1*(1-x),
                "alpha": 1
                },
            "arbres_prop": {
                "edges_path": edges_buffer_arbres_prop_path,
                # "fn": lambda x: 1 if x>=0.6 else(5 if x>=0.2 and x<0.6 else 20),
                "fn_cont": lambda x: 10*(1-x),
                "alpha": 10
                },
            "C_wavg_scaled": {
                "edges_path": edges_buffer_temp_wavg_path,
                # "fn": lambda x: 1 if x<33 else(5 if x>=33 and x<37 else 10),
                "fn_cont": lambda x: 1*(1-x),
                "alpha": 1
                },
            "eaux_prop": {
                "edges_path": edges_buffer_eaux_prop_path,
                # "fn": lambda x: 1 if x > 0.7 else(3 if x >= 0.3 and x <=0.7 else 7),
                "fn_cont": lambda x: 1*(1-x),
                "alpha": 1
                },
            "canop": {
                "edges_path": edges_buffer_parcs_prop_path,
                # "fn": lambda x: 1 if x=="high" else(8 if x =="medium" else 15),
                "fn_cont": lambda x: 1*(1-x),
                "alpha": 1
                },
        }
    }
}

meta_params_2807 = {
    "P0_01O0_01At0_01Ar10C0_01E0_01Ca0_01" : {
        "graph_path": "./output_data/network/graph/final_network_P0_01O0_01At0_01Ar10C0_01E0_01Ca0_01.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            # "fn": lambda x: 1 if x>=0.4 else(3 if x>=0.2 and x<0.4 else 5),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(5 if x>=0.2 and x<0.6 else 20),
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            # "fn": lambda x: 1 if x<33 else(5 if x>=33 and x<37 else 10),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            # "fn": lambda x: 1 if x > 0.7 else(3 if x >= 0.3 and x <=0.7 else 7),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            # "fn": lambda x: 1 if x=="high" else(8 if x =="medium" else 15),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        },
    },
    "P0_01O0_01At0_01Ar100C0_01E0_01Ca0_01" : {
        "graph_path": "./output_data/network/graph/final_network_P0_01O0_01At0_01Ar100C0_01E0_01Ca0_01.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            # "fn": lambda x: 1 if x>=0.4 else(3 if x>=0.2 and x<0.4 else 5),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(5 if x>=0.2 and x<0.6 else 20),
            "fn_cont": lambda x: 100*(1-x),
            "alpha": 100
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            # "fn": lambda x: 1 if x<33 else(5 if x>=33 and x<37 else 10),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            # "fn": lambda x: 1 if x > 0.7 else(3 if x >= 0.3 and x <=0.7 else 7),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            # "fn": lambda x: 1 if x=="high" else(8 if x =="medium" else 15),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        },
    },
    
}

meta_params_0708 = {
    "P0_01O9At0_01Ar10C0_01E0_01Ca0_01" : {
        "graph_path": "./output_data/network/graph/final_network_P0_01O9At0_01Ar10C0_01E0_01Ca0_01.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 9*(1-x),
            "alpha": 9
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 9*(1-x),
            "alpha": 9
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 9*(1-x),
            "alpha": 9
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            # "fn": lambda x: 1 if x>=0.4 else(3 if x>=0.2 and x<0.4 else 5),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(5 if x>=0.2 and x<0.6 else 20),
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            # "fn": lambda x: 1 if x<33 else(5 if x>=33 and x<37 else 10),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            # "fn": lambda x: 1 if x > 0.7 else(3 if x >= 0.3 and x <=0.7 else 7),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            # "fn": lambda x: 1 if x=="high" else(8 if x =="medium" else 15),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        },
    },
    "P0_01O7At0_01Ar10C0_01E0_01Ca0_01" : {
        "graph_path": "./output_data/network/graph/final_network_P0_01O7At0_01Ar10C0_01E0_01Ca0_01.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 7*(1-x),
            "alpha": 7
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 7*(1-x),
            "alpha": 7
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 7*(1-x),
            "alpha": 7
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            # "fn": lambda x: 1 if x>=0.4 else(3 if x>=0.2 and x<0.4 else 5),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(5 if x>=0.2 and x<0.6 else 20),
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            # "fn": lambda x: 1 if x<33 else(5 if x>=33 and x<37 else 10),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            # "fn": lambda x: 1 if x > 0.7 else(3 if x >= 0.3 and x <=0.7 else 7),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            # "fn": lambda x: 1 if x=="high" else(8 if x =="medium" else 15),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        },
    },
    "P0_01O5At0_01Ar10C0_01E0_01Ca0_01" : {
        "graph_path": "./output_data/network/graph/final_network_P0_01O5At0_01Ar10C0_01E0_01Ca0_01.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            # "fn": lambda x: 1 if x>=0.4 else(3 if x>=0.2 and x<0.4 else 5),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(5 if x>=0.2 and x<0.6 else 20),
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            # "fn": lambda x: 1 if x<33 else(5 if x>=33 and x<37 else 10),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            # "fn": lambda x: 1 if x > 0.7 else(3 if x >= 0.3 and x <=0.7 else 7),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            # "fn": lambda x: 1 if x=="high" else(8 if x =="medium" else 15),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        },
    },
    "P0_01O3At0_01Ar10C0_01E0_01Ca0_01" : {
        "graph_path": "./output_data/network/graph/final_network_P0_01O3At0_01Ar10C0_01E0_01Ca0_01.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 3*(1-x),
            "alpha": 3
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 3*(1-x),
            "alpha": 3
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 3*(1-x),
            "alpha": 3
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            # "fn": lambda x: 1 if x>=0.4 else(3 if x>=0.2 and x<0.4 else 5),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(5 if x>=0.2 and x<0.6 else 20),
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            # "fn": lambda x: 1 if x<33 else(5 if x>=33 and x<37 else 10),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            # "fn": lambda x: 1 if x > 0.7 else(3 if x >= 0.3 and x <=0.7 else 7),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            # "fn": lambda x: 1 if x=="high" else(8 if x =="medium" else 15),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        },
    },
    "P0_01O1At0_01Ar10C0_01E0_01Ca0_01" : {
        "graph_path": "./output_data/network/graph/final_network_P0_01O1At0_01Ar10C0_01E0_01Ca0_01.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 1*(1-x),
            "alpha": 1
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 1*(1-x),
            "alpha": 1
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 1*(1-x),
            "alpha": 1
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            # "fn": lambda x: 1 if x>=0.4 else(3 if x>=0.2 and x<0.4 else 5),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(5 if x>=0.2 and x<0.6 else 20),
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            # "fn": lambda x: 1 if x<33 else(5 if x>=33 and x<37 else 10),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            # "fn": lambda x: 1 if x > 0.7 else(3 if x >= 0.3 and x <=0.7 else 7),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            # "fn": lambda x: 1 if x=="high" else(8 if x =="medium" else 15),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        },
    },  
}

meta_params_1008 = {
        "P0_01O10At0_01Ar0_01C0_01E0_01Ca0_01" : {
        "graph_path": "./output_data/network/graph/final_network_P0_01O10At0_01Ar0_01C0_01E0_01Ca0_01.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            # "fn": lambda x: 1 if x>=0.4 else(3 if x>=0.2 and x<0.4 else 5),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(5 if x>=0.2 and x<0.6 else 20),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            # "fn": lambda x: 1 if x<33 else(5 if x>=33 and x<37 else 10),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            # "fn": lambda x: 1 if x > 0.7 else(3 if x >= 0.3 and x <=0.7 else 7),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            # "fn": lambda x: 1 if x=="high" else(8 if x =="medium" else 15),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        },
    },
    "P0_01O0_0At0_01Ar0_01C0_01E0_01Ca10" : {
        "graph_path": "./output_data/network/graph/final_network_P0_01O0_01At0_01Ar0_01C0_01E0_01Ca10.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            # "fn": lambda x: 1 if x>=0.4 else(3 if x>=0.2 and x<0.4 else 5),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(5 if x>=0.2 and x<0.6 else 20),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            # "fn": lambda x: 1 if x<33 else(5 if x>=33 and x<37 else 10),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            # "fn": lambda x: 1 if x > 0.7 else(3 if x >= 0.3 and x <=0.7 else 7),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            # "fn": lambda x: 1 if x=="high" else(8 if x =="medium" else 15),
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        },
    },
    "P0_01O10At0_01Ar10C0_01E0_01Ca10" : {
        "graph_path": "./output_data/network/graph/final_network_P0_01O10At0_01Ar10C0_01E0_01Ca10.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            # "fn": lambda x: 1 if x>=0.4 else(3 if x>=0.2 and x<0.4 else 5),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(5 if x>=0.2 and x<0.6 else 20),
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            # "fn": lambda x: 1 if x<33 else(5 if x>=33 and x<37 else 10),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            # "fn": lambda x: 1 if x > 0.7 else(3 if x >= 0.3 and x <=0.7 else 7),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            # "fn": lambda x: 1 if x=="high" else(8 if x =="medium" else 15),
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        },
    },
}

meta_params_1008_2 = {
        "P0_01O0_01At0_01Ar0_01C10E0_01Ca0_01" : {
        "graph_path": "./output_data/network/graph/final_network_P0_01O0_01At0_01Ar0_01C10E0_01Ca0_01.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            # "fn": lambda x: 1 if x>=0.4 else(3 if x>=0.2 and x<0.4 else 5),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(5 if x>=0.2 and x<0.6 else 20),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            # "fn": lambda x: 1 if x<33 else(5 if x>=33 and x<37 else 10),
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            # "fn": lambda x: 1 if x > 0.7 else(3 if x >= 0.3 and x <=0.7 else 7),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            # "fn": lambda x: 1 if x=="high" else(8 if x =="medium" else 15),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        },
    },
    "P0_01O0_01At0_01Ar10C0_01E0_01Ca9" : {
        "graph_path": "./output_data/network/graph/final_network_P0_01O0_01At0_01Ar10C0_01E0_01Ca9.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            # "fn": lambda x: 1 if x>=0.4 else(3 if x>=0.2 and x<0.4 else 5),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(5 if x>=0.2 and x<0.6 else 20),
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            # "fn": lambda x: 1 if x<33 else(5 if x>=33 and x<37 else 10),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            # "fn": lambda x: 1 if x > 0.7 else(3 if x >= 0.3 and x <=0.7 else 7),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            # "fn": lambda x: 1 if x=="high" else(8 if x =="medium" else 15),
            "fn_cont": lambda x: 9*(1-x),
            "alpha": 9
            },
        },
    },
    "P0_01O0_01At0_01Ar10C0_01E0_01Ca7" : {
        "graph_path": "./output_data/network/graph/final_network_P0_01O0_01At0_01Ar10C0_01E0_01Ca7.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            # "fn": lambda x: 1 if x>=0.4 else(3 if x>=0.2 and x<0.4 else 5),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(5 if x>=0.2 and x<0.6 else 20),
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            # "fn": lambda x: 1 if x<33 else(5 if x>=33 and x<37 else 10),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            # "fn": lambda x: 1 if x > 0.7 else(3 if x >= 0.3 and x <=0.7 else 7),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            # "fn": lambda x: 1 if x=="high" else(8 if x =="medium" else 15),
            "fn_cont": lambda x: 7*(1-x),
            "alpha": 7
            },
        },
    },
    "P0_01O0_01At0_01Ar10C0_01E0_01Ca5" : {
        "graph_path": "./output_data/network/graph/final_network_P0_01O0_01At0_01Ar10C0_01E0_01Ca5.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            # "fn": lambda x: 1 if x>=0.4 else(3 if x>=0.2 and x<0.4 else 5),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(5 if x>=0.2 and x<0.6 else 20),
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            # "fn": lambda x: 1 if x<33 else(5 if x>=33 and x<37 else 10),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            # "fn": lambda x: 1 if x > 0.7 else(3 if x >= 0.3 and x <=0.7 else 7),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            # "fn": lambda x: 1 if x=="high" else(8 if x =="medium" else 15),
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        },
    },
    "P0_01O0_01At0_01Ar10C0_01E0_01Ca3" : {
        "graph_path": "./output_data/network/graph/final_network_P0_01O0_01At0_01Ar10C0_01E0_01Ca3.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            # "fn": lambda x: 1 if x>=0.4 else(3 if x>=0.2 and x<0.4 else 5),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(5 if x>=0.2 and x<0.6 else 20),
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            # "fn": lambda x: 1 if x<33 else(5 if x>=33 and x<37 else 10),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            # "fn": lambda x: 1 if x > 0.7 else(3 if x >= 0.3 and x <=0.7 else 7),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            # "fn": lambda x: 1 if x=="high" else(8 if x =="medium" else 15),
            "fn_cont": lambda x: 3*(1-x),
            "alpha": 3
            },
        },
    },
    "P0_01O0_01At0_01Ar10C0_01E0_01Ca1" : {
        "graph_path": "./output_data/network/graph/final_network_P0_01O0_01At0_01Ar10C0_01E0_01Ca1.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            # "fn": lambda x: 1 if x>=0.4 else(3 if x>=0.2 and x<0.4 else 5),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(5 if x>=0.2 and x<0.6 else 20),
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            # "fn": lambda x: 1 if x<33 else(5 if x>=33 and x<37 else 10),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            # "fn": lambda x: 1 if x > 0.7 else(3 if x >= 0.3 and x <=0.7 else 7),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            # "fn": lambda x: 1 if x=="high" else(8 if x =="medium" else 15),
            "fn_cont": lambda x: 1*(1-x),
            "alpha": 1
            },
        },
    },
}

meta_params_1108 = {
        "P0_01O9At0_01Ar10C0_01E0_01Ca3" : {
        "graph_path": "./output_data/network/graph/final_network_P0_01O9At0_01Ar10C0_01E0_01Ca3.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 9*(1-x),
            "alpha": 9
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 9*(1-x),
            "alpha": 9
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 9*(1-x),
            "alpha": 9
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            # "fn": lambda x: 1 if x>=0.4 else(3 if x>=0.2 and x<0.4 else 5),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(5 if x>=0.2 and x<0.6 else 20),
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            # "fn": lambda x: 1 if x<33 else(5 if x>=33 and x<37 else 10),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            # "fn": lambda x: 1 if x > 0.7 else(3 if x >= 0.3 and x <=0.7 else 7),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            # "fn": lambda x: 1 if x=="high" else(8 if x =="medium" else 15),
            "fn_cont": lambda x: 3*(1-x),
            "alpha": 3
            },
        },
    },
    "P0_01O7At0_01Ar10C0_01E0_01Ca3" : {
        "graph_path": "./output_data/network/graph/final_network_P0_01O7At0_01Ar10C0_01E0_01Ca3.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 7*(1-x),
            "alpha": 7
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 7*(1-x),
            "alpha": 7
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 7*(1-x),
            "alpha": 7
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            # "fn": lambda x: 1 if x>=0.4 else(3 if x>=0.2 and x<0.4 else 5),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(5 if x>=0.2 and x<0.6 else 20),
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            # "fn": lambda x: 1 if x<33 else(5 if x>=33 and x<37 else 10),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            # "fn": lambda x: 1 if x > 0.7 else(3 if x >= 0.3 and x <=0.7 else 7),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            # "fn": lambda x: 1 if x=="high" else(8 if x =="medium" else 15),
            "fn_cont": lambda x: 3*(1-x),
            "alpha": 3
            },
        },
    },
    "P0_01O5At0_01Ar10C0_01E0_01Ca3" : {
        "graph_path": "./output_data/network/graph/final_network_P0_01O5At0_01Ar10C0_01E0_01Ca3.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            # "fn": lambda x: 1 if x>=0.4 else(3 if x>=0.2 and x<0.4 else 5),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(5 if x>=0.2 and x<0.6 else 20),
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            # "fn": lambda x: 1 if x<33 else(5 if x>=33 and x<37 else 10),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            # "fn": lambda x: 1 if x > 0.7 else(3 if x >= 0.3 and x <=0.7 else 7),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            # "fn": lambda x: 1 if x=="high" else(8 if x =="medium" else 15),
            "fn_cont": lambda x: 3*(1-x),
            "alpha": 3
            },
        },
    },
    "P0_01O3At0_01Ar10C0_01E0_01Ca3" : {
        "graph_path": "./output_data/network/graph/final_network_P0_01O3At0_01Ar10C0_01E0_01Ca3.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 3*(1-x),
            "alpha": 3
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 3*(1-x),
            "alpha": 3
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 3*(1-x),
            "alpha": 3
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            # "fn": lambda x: 1 if x>=0.4 else(3 if x>=0.2 and x<0.4 else 5),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(5 if x>=0.2 and x<0.6 else 20),
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            # "fn": lambda x: 1 if x<33 else(5 if x>=33 and x<37 else 10),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            # "fn": lambda x: 1 if x > 0.7 else(3 if x >= 0.3 and x <=0.7 else 7),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            # "fn": lambda x: 1 if x=="high" else(8 if x =="medium" else 15),
            "fn_cont": lambda x: 3*(1-x),
            "alpha": 3
            },
        },
    },
    "P0_01O1At0_01Ar10C0_01E0_01Ca3" : {
        "graph_path": "./output_data/network/graph/final_network_P0_01O1At0_01Ar10C0_01E0_01Ca3.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 1*(1-x),
            "alpha": 1
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 1*(1-x),
            "alpha": 1
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(2 if x>=0.2 and x<0.6 else 3),
            "fn_cont": lambda x: 1*(1-x),
            "alpha": 1
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            # "fn": lambda x: 1 if x>=0.4 else(3 if x>=0.2 and x<0.4 else 5),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            # "fn": lambda x: 1 if x>=0.6 else(5 if x>=0.2 and x<0.6 else 20),
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            # "fn": lambda x: 1 if x<33 else(5 if x>=33 and x<37 else 10),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            # "fn": lambda x: 1 if x > 0.7 else(3 if x >= 0.3 and x <=0.7 else 7),
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            # "fn": lambda x: 1 if x=="high" else(8 if x =="medium" else 15),
            "fn_cont": lambda x: 3*(1-x),
            "alpha": 3
            },
        },
    },
}

#### ATTENTION, pas alpha*(1-x) pour la température mais bien alpha*x !! 

meta_params_1308 = {
        "P0_01O0_01At0_01Ar0_01C10E0_01Ca0_01" : {
        "graph_path": "./output_data/network/graph/final_network_P0_01O5At0_01Ar10C9E0_01Ca0_01.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            "fn_cont": lambda x: 10*x,
            "alpha": 10
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        },
    },
    "P0_01O5At0_01Ar10C9E0_01Ca0_01" : {
        "graph_path": "./output_data/network/graph/final_network_P0_01O5At0_01Ar10C9E0_01Ca0_01.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            "fn_cont": lambda x: 9*x,
            "alpha": 9
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        },
    },
    "P0_01O5At0_01Ar10C7E0_01Ca0_01" : {
        "graph_path": "./output_data/network/graph/final_network_P0_01O5At0_01Ar10C7E0_01Ca0_01.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            "fn_cont": lambda x: 7*x,
            "alpha": 7
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        },
    },
    "P0_01O5At0_01Ar10C5E0_01Ca0_01" : {
        "graph_path": "./output_data/network/graph/final_network_P0_01O5At0_01Ar10C5E0_01Ca0_01.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            "fn_cont": lambda x: 5*x,
            "alpha": 5
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        },
    },
    "P0_01O5At0_01Ar10C3E0_01Ca0_01" : {
        "graph_path": "./output_data/network/graph/final_network_P0_01O5At0_01Ar10C3E0_01Ca0_01.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            "fn_cont": lambda x: 3*x,
            "alpha": 3
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        },
    },
    "P0_01O5At0_01Ar10C1E0_01Ca0_01" : {
        "graph_path": "./output_data/network/graph/final_network_P0_01O5At0_01Ar10C1E0_01Ca0_01.gpkg",
        "params": {
            "prairies_prop" : {
            "edges_path": edges_buffer_prairies_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "ombres_08_prop" : {
            "edges_path": edges_buffer_ombres_08_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "ombres_13_prop" : {
            "edges_path": edges_buffer_ombres_13_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "ombres_18_prop" : {
            "edges_path": edges_buffer_ombres_18_prop_path,
            "fn_cont": lambda x: 5*(1-x),
            "alpha": 5
            },
        "arbustes_prop": {
            "edges_path": edges_buffer_arbustes_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "arbres_prop": {
            "edges_path": edges_buffer_arbres_prop_path,
            "fn_cont": lambda x: 10*(1-x),
            "alpha": 10
            },
        "C_wavg_scaled": {
            "edges_path": edges_buffer_temp_wavg_path,
            "fn_cont": lambda x: 1*x,
            "alpha": 1
            },
        "eaux_prop": {
            "edges_path": edges_buffer_eaux_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        "canop": {
            "edges_path": edges_buffer_parcs_prop_path,
            "fn_cont": lambda x: 0.01*(1-x),
            "alpha": 0.01
            },
        },
    },
}

#%%
score_calculation_pipeline(meta_params_1308)

#%%
#all_score_edges(edges_buffer_path, edges_buffer_scored_path, params)

#%%
# one_score_edges(edges_buffer_scored_path, edges_buffer_scored_path, params, key="ombres_08_prop")
# one_score_edges(edges_buffer_scored_path, edges_buffer_scored_path, params, key="ombres_13_prop")
# one_score_edges(edges_buffer_scored_path, edges_buffer_scored_path, params, key="ombres_18_prop")

# clip_bouding_data(edges_buffer_scored_path, bouding_mask_path, edges_buffer_scored_bounding_path)

#%%
# total_score(edges_buffer_scored_path, edges_buffer_total_score_path, score_columns)
# score_distance(edges_buffer_total_score_path, edges_buffer_total_score_distance_path,0.5,0.5)
# score_fraicheur(edges_buffer_total_score_distance_path, edges_buffer_total_score_distance_freshness_path)

# clip_bouding_graph(metrop_network_path, bouding_mask_path, metrop_network_bounding_path)

#%%
# create_graph(metrop_network_path, edges_buffer_total_score_distance_freshness_path, final_network_path)


#%%
# weights_path = "./weights_score.csv"

# # Check if the weights file is empty
# try:
#     weights = pd.read_csv(weights_path)
# except pd.errors.EmptyDataError:
#     # If the file is empty, create a new DataFrame with columns
#     weights = pd.DataFrame(columns=["graph_file", "arbres", "ombres" "arbustes", "prairies", "temp", "canop", "eaux"])

# currents_weights = pd.DataFrame({
#     "graph_file": final_network_path,
#     "arbres": params["arbres_prop"]["alpha"],
#     "ombres": params["ombres_08_prop"]["alpha"],
#     "arbustes": params["arbustes_prop"]["alpha"],
#     "prairies": params["prairies_prop"]["alpha"],
#     "temp": params["C_wavg_scaled"]["alpha"],
#     "canop": params["canop"]["alpha"],
#     "eaux": params["eaux_prop"]["alpha"]
# }, index=[0])

# concat_weights = pd.concat([weights, currents_weights])

# concat_weights.to_csv(weights_path, index=False)

#%%

# all_prop(edges_buffer_path, params, "output_data/analyse/edges_all_prop.gpkg")
# %%
