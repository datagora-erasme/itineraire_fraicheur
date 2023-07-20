#%%
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
from scipy.stats import ttest_rel
#%%
## FUNCTION : 
def load_graph_from_pickle(pickle_path):
    # Load the graph from the pickle file
    with open(pickle_path, 'rb') as f:
        G = pickle.load(f)

    return G

def shortest_path(G, start, end, G_multidigraph, index, global_gdf, min_dist=200):
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

    if(sum_distance >= min_dist):
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


def create_random_itineraries(nodes_path, graph_path, multidigraph_path, n_itineraries, itineraries_path, min_dist=200):
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
        global_gdf = shortest_path(G, start, end, MG, count, global_gdf, min_dist=min_dist)
        count+=1

    print("saving file")
    global_gdf.to_file(itineraries_path, driver="GPKG", layer="itineraries")
    print("ALL DONE")

def extract_frequency_scores(sample_itineraries_path, output_folder_path, zone_name):
    itineraries = gpd.read_file(sample_itineraries_path, layer="itineraries")
    itineraries_if = itineraries[itineraries["type"] == "IF"]
    itineraries_len = itineraries[itineraries["type"] == "LEN"]

    freq_edges_if = gpd.GeoDataFrame({
        "count": itineraries_if.groupby(["u", "v", "key"])["total_score"].count(),
        "score": itineraries_if.groupby(["u", "v", "key"])["total_score"].apply(lambda x: round(x.unique()[0])),
        "geometry": itineraries_if.groupby(["u", "v", "key"])["geometry"].apply(lambda x: x.unique()[0])
    })

    freq_edges_if.to_file(f"{output_folder_path}{zone_name}/count_freq_if_{zone_name}.gpkg", driver="GPKG", layer="edges")

    freq_edges_len = gpd.GeoDataFrame({
        "count": itineraries_len.groupby(["u", "v", "key"])["total_score"].count(),
        "score": itineraries_len.groupby(["u", "v", "key"])["total_score"].apply(lambda x: round(x.unique()[0])),
        "geometry": itineraries_len.groupby(["u", "v", "key"])["geometry"].apply(lambda x: x.unique()[0])
    })

    freq_edges_len.to_file(f"{output_folder_path}{zone_name}/count_freq_len_{zone_name}.gpkg", driver="GPKG", layer="edges")

def calculate_mean_score(it):
    """Calculate the mean score for a given itinerary"""
    return round(sum(it["score_distance"])/sum(it["length"]), 2)

def create_df_mean_score(itineraries_path):
    "calculate mean score for every itineraries of a file"
    itineraries = gpd.read_file(itineraries_path)
    
    it_score = itineraries[["id_it", "type", "score_distance", "length"]].groupby(["id_it", "type"], axis=0).apply(calculate_mean_score).reset_index(name="score")
    it_length = itineraries[["id_it", "type", "score_distance", "length"]].groupby(["id_it", "type"], axis=0).apply(lambda x: round(sum(x["length"]),2)).reset_index(name="total_length")
    it_score["total_length"] = it_length["total_length"]

    print("it_score: ", it_score)
    it_score.to_csv("./output_data/analyse/results.csv")

def test_students(group1, group2):
    """In order to compare the mean between the distribution of group 1 and group 2"""
    return ttest_rel(group1, group2)

def d_cohen(group1, group2):
    """In order to know if there is a size effect"""
    mean1 = np.mean(group1)
    mean2 = np.mean(group2)

    var1 = np.var(group1, ddof=1)
    var2 = np.var(group2, ddof=2)
    
    n1 = len(group1)
    n2 = len(group2)

    pooled_std = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))

    return (mean1 - mean2) / pooled_std

def distance_cost(group1, group2):
    """Calculate the distance cost between itineraries"""
    d1 = np.array(group1["total_length"])
    d2 = np.array(group2["total_length"])

    percent_diff = ((d2-d1)/d1)*100

    return round(np.mean(percent_diff),2)

## GLOBAL VARIABLES
zones_path = "./input_data/studies_zones/studies_sectors.gpkg"
graph_path = "./output_data/network/graph/final_network_bounding_scaled_no_na.gpkg"
clipped_nodes_tetedor_path = "./output_data/studies_zones/tetedor_nodes.gpkg"
clipped_nodes_partdieu_path = "./output_data/studies_zones/partdieu/partdieu_nodes.gpkg"
clipped_nodes_rillieux_path = "./output_data/studies_zones/rillieux/rillieux_nodes.gpkg"
clipped_nodes_confluence_path = "./output_data/studies_zones/confluence/confluence_nodes.gpkg"
clipped_nodes_metropole_path = "./output_data/studies_zones/metropole/metropole_nodes.gpkg"

graph_pickle = "./output_data/network/graph/final_network_bounding_scaled_no_na.pickle"
multidigraph_pickle = "./output_data/network/graph/final_network_bounding_scaled_no_na_multidigraph.pickle"

tetedor_itineraries_path = "./output_data/studies_zones/tetedor/100_it.gpkg"
partdieu_itineraries_path = "./output_data/studies_zones/partdieu/partdieu_100_it.gpkg"
rillieux_itineraries_path = "./output_data/studies_zones/rillieux/rillieux_100_it.gpkg"
confluence_itineraries_path = "./output_data/studies_zones/confluence/confluence_100_it.gpkg"
metropole_itineraries_path = "./output_data/studies_zones/metropole/metropole_5000_it.gpkg"

output_folder_path = "./output_data/studies_zones/"

#%%
## SCRIPT

### TETE D'OR

# clipp_graph_nodes_from_zone(zones_path, "tetedor", graph_path, clipped_nodes_tetedor_path)
# create_random_itineraries(clipped_nodes_tetedor_path, graph_pickle, multidigraph_pickle, 200, tetedor_itineraries_path)

## PART DIEU
# clipp_graph_nodes_from_zone(zones_path, "partdieu", graph_path, clipped_nodes_partdieu_path)
# create_random_itineraries(clipped_nodes_partdieu_path, graph_pickle, multidigraph_pickle, 200, partdieu_itineraries_path)

## RILLIEUX LA PAPE

# clipp_graph_nodes_from_zone(zones_path, "rillieux", graph_path, clipped_nodes_rillieux_path)
# create_random_itineraries(clipped_nodes_rillieux_path, graph_pickle, multidigraph_pickle, 200, rillieux_itineraries_path)

## CONFLUENCE

# clipp_graph_nodes_from_zone(zones_path, "confluence", graph_path, clipped_nodes_confluence_path)
# create_random_itineraries(clipped_nodes_confluence_path, graph_pickle, multidigraph_pickle, 200, confluence_itineraries_path)
# extract_frequency_scores(confluence_itineraries_path, output_folder_path, "confluence")

## METROP 

# clipp_graph_nodes_from_zone(zones_path, "metropole", graph_path, clipped_nodes_metropole_path)
# create_random_itineraries(clipped_nodes_metropole_path, graph_pickle, multidigraph_pickle, 1000, metropole_itineraries_path, min_dist=500)
# extract_frequency_scores(metropole_itineraries_path, output_folder_path, "metropole")

# create_df_mean_score(metropole_itineraries_path)

# weights_score = pd.read_csv("./output_data/analyse/results.csv")

# score_if = weights_score[weights_score["type"] == "IF"]["score"]
# score_len = weights_score[weights_score["type"] == "LEN"]["score"]

# len_if = weights_score[weights_score["type"] == "IF"]["total_length"]
# len_len = weights_score[weights_score["type"] == "LEN"]["total_length"]

# # Les deux groupes sont dépendants (ind stats = couple départ et arrivée) + la distance est prise en compte dans les deux cas
# t_test_score = test_students(score_len, score_if)
# d_score = d_cohen(score_len, score_if)

# print("ttest : ", t_test_score) # TtestResult(statistic=41.14863591276434, pvalue=1.7158511760401674e-162, df=499)
# print("d de cohen : ", d_score) # 1.8976097648251313 
# # On peut rejetter H0, la différence entre les deux n'est pas due au hasard. 

# t_test_len = test_students(len_len, len_if)
# d_len = d_cohen(len_len, len_if)

# print("ttest len :", t_test_len) #TtestResult(statistic=-27.57299161407194, pvalue=2.2809899288342848e-102, df=499)
# print("d cohen len : ", d_len) #-0.18036484141490464

# #On rejette H0 : les trajets sont en moyennes plus longs pour les itinéraires les plus frais (logique) mais la taille de l'effet est faible

# d_cost = distance_cost(weights_score[weights_score["type"] == "LEN"], weights_score[weights_score["type"] == "IF"])

# print(f"cost distance : {d_cost} %") # faire la distrib et regarder les quantiles plutôt que la moyenne du coût

#%%

count_freq_if = gpd.read_file(output_folder_path + "metropole/count_freq_if_metropole.gpkg")
count_freq_len = gpd.read_file(output_folder_path + "metropole/count_freq_len_metropole.gpkg")

count_freq_if = count_freq_if.set_index(["u", "v", "key"])
count_freq_len = count_freq_len.set_index(["u", "v", "key"])

count_all_freq = count_freq_if.merge(count_freq_len, on=["u", "v", "key"], how="outer", suffixes=("_if", "_len"))

count_all_freq = count_all_freq.drop(["geometry_if", "geometry_len"], axis=1)

count_all_freq = count_all_freq.fillna(0) #si na => pas fréquenté

#count_freq_if.to_file(output_folder_path + "metropole/count_all_freq.gpkg", driver="GPKG", layer="edges")
# %%

freq_if = count_all_freq["count_if"].astype(float)
freq_len = count_all_freq["count_len"].astype(float)

ttest_freq = test_students(freq_len, freq_if)
d_freq = d_cohen(freq_len, freq_if)

print(ttest_freq)
print(d_freq) #pour l'ensemble metrop pas d'effet mais du à la nature des itinéraires..

# %%

print(count_freq_len.isna().sum())
print(len(count_freq_len))
print(len(count_freq_if))
# %%

# %%
