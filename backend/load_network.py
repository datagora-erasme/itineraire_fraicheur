import os
os.environ['USE_PYGEOS'] = '0'
import networkx as nx
import geopandas as gpd
import osmnx as ox
import pickle
import time
import sys


def load_network(network_path, pickle_path, network_multidigraph_pickle_path):
    gdf_edges = gpd.read_file(network_path, layer='edges')
    gdf_nodes = gpd.read_file(network_path, layer="nodes")

    gdf_nodes["y"] = gdf_nodes["lat"]
    gdf_nodes["x"] = gdf_nodes["lon"]

    #remove unecessary columns in order to lightened the network
    new_edges = gdf_edges[["u", "v", "key", "osmid", "length", "from", "to", "score_distance", "total_score", "freshness_score", "score_distance_prop", "exp_distance","exp_fresh_score", "exp_fresh_score_15", "geometry"]].set_geometry("geometry")
    new_edges.to_crs(gdf_edges.crs)

    new_edges = new_edges.set_index(["u", "v", "key"])
    gdf_nodes = gdf_nodes.set_index(['osmid'])

    G = ox.graph_from_gdfs(gdf_nodes, new_edges)

    G2 = nx.Graph(G)
    # G2 = nx.MultiDiGraph(G)

    G_digraph = nx.MultiDiGraph(G2)

    with open(pickle_path, "wb") as f:
        pickle.dump(G2, f)

    with open(network_multidigraph_pickle_path, "wb") as f:
        pickle.dump(G_digraph, f)
    return True

# network_path = sys.argv[1]
# pickle_path = sys.argv[2]
# # s = time.time()
# load_graph(network_path, pickle_path)
# e = time.time()
# print(f"duration : {e-s}")