import os
os.environ['USE_PYGEOS'] = '0'
import networkx as nx
import geopandas as gpd
import osmnx as ox
import pickle

def create_pickles_from_graph(graph_path, graph_pickle_path, graph_multidigraph_pickle_path):
    """
        Load a graph into pickles files. \n
        Both simple graph and multidigraph are needed for the function shortest_path of the project.
    """
    gdf_edges = gpd.read_file(graph_path, layer='edges')
    gdf_nodes = gpd.read_file(graph_path, layer="nodes")

    gdf_nodes["y"] = gdf_nodes["lat"]
    gdf_nodes["x"] = gdf_nodes["lon"]

    #remove unecessary columns in order to lightened the graph
    new_edges = gdf_edges[["u", "v", "key", "osmid", "length", "from", "to", "score_distance_13", "total_score_13", "freshness_score", "geometry"]].set_geometry("geometry")
    new_edges.to_crs(gdf_edges.crs)

    new_edges = new_edges.set_index(["u", "v", "key"])
    gdf_nodes = gdf_nodes.set_index(['osmid'])

    G = ox.graph_from_gdfs(gdf_nodes, new_edges)

    G2 = nx.Graph(G)

    G_digraph = nx.MultiDiGraph(G2)

    with open(graph_pickle_path, "wb") as f:
        pickle.dump(G2, f)

    with open(graph_multidigraph_pickle_path, "wb") as f:
        pickle.dump(G_digraph, f)
    return True

def load_graph_from_pickle(pickle_path):
    """Load a graph from a pickle file"""
    with open(pickle_path, 'rb') as f:
        G = pickle.load(f)

    return G