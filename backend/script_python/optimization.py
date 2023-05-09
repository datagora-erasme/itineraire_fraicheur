import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
import networkx as nx
import osmnx as ox
import random
import traceback
import math
import time
import csv

"""This file will not be use in production. It has been made in order to optimize
and choose the best algorithm to find the shortest path in the network"""

metrop_graph_path = "./data/osm/final_network.gpkg"
output_folder = "./script_python/optimization_files/"

output_optimization_folder = "./script_python/optimization_files/"
csv_results_path = "./script_python/optimization_files/results.csv"

def select_random_nodes(nb_nodes, graph_path, output_start_path, output_end_path):
    """This function select nb_nodes start and end nodes from a graph and save them into a gpkg file"""

    edges = gpd.read_file(graph_path, layer="edges")
    nodes = gpd.read_file(graph_path, layer="nodes")

    edges = edges.set_index(["u", "v", "key"])
    nodes = nodes.set_index(["osmid"])

    G = ox.graph_from_gdfs(nodes, edges)

    start_nodes = random.sample(G.nodes, nb_nodes)
    end_nodes = random.sample(G.nodes, nb_nodes)

    start_points = gpd.GeoDataFrame(geometry=gpd.points_from_xy([G.nodes[node]['x'] for node in start_nodes],
                                                            [G.nodes[node]['y'] for node in start_nodes]))
    end_points = gpd.GeoDataFrame(geometry=gpd.points_from_xy([G.nodes[node]['x'] for node in end_nodes],
                                                          [G.nodes[node]['y'] for node in end_nodes]))
    start_points.to_file(output_start_path, layer='start_points', driver='GPKG')
    end_points.to_file(output_end_path, layer='end_points', driver='GPKG')


#select_random_nodes(3, metrop_graph_path, output_folder + "start_nodes.gpkg", output_folder + "end_nodes.gpkg")

def euclidian_distance(node1, node2, G):
    # print(G.nodes[node1])
    (x1, y1) = G.nodes[node1]["x"], G.nodes[node1]["y"]
    (x2, y2)= G.nodes[node2]["x"], G.nodes[node1]["y"]

    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def manhattan_distance(node1, node2):
    (x1, y1) = node1
    (x2, y2)= node2

    return abs(x2 - x1) + abs(y2 - y1)

def sp(graph_path, start, end, weight, shortest_path_file_path, algorithm, heuristic=None):
    # Load the graph data from the GeoPackage file
    start = time.time()
    gdf_edges = gpd.read_file(graph_path, layer='edges')
    gdf_nodes = gpd.read_file(graph_path, layer="nodes")
    end = time.time()
    print((end-start)/60)

    gdf_edges = gdf_edges.set_index(['u', 'v', 'key'])
    gdf_nodes = gdf_nodes.set_index(['osmid'])

    gdf_nodes["y"] = gdf_nodes["lat"]
    gdf_nodes["x"] = gdf_nodes["lon"]

    G = ox.graph_from_gdfs(gdf_nodes, gdf_edges)

    G2 = nx.Graph(G)

    origin_node = ox.nearest_nodes(G2, X=start[1], Y=start[0])
    destination_node = ox.nearest_nodes(G2, X=end[1], Y=end[0])

    try:
        # Calculate the shortest path using Dijkstra's algorithm
        if(algorithm == "Dijkstra"):
            shortest_path = nx.shortest_path(G2, source=origin_node, target=destination_node, weight=weight)
        
        elif(algorithm == "Alpha_star"):
            shortest_path = nx.astar_path(G2, source=origin_node, target=destination_node, weight=weight, heuristic=lambda u,v : heuristic(u,v,G2))

        G3 = nx.MultiDiGraph(G2)

        route_edges = ox.utils_graph.get_route_edge_attributes(G3, shortest_path)

        gdf_route_edges = gpd.GeoDataFrame(route_edges, crs=G.graph['crs'], geometry='geometry')

        gdf_route_edges = gdf_route_edges.to_crs(epsg=3946)

        gdf_route_edges.to_file(shortest_path_file_path, driver='GPKG')

    except nx.NetworkXNoPath:
        traceback.print_exc()
        print("No path found")

def optimization(graph_path, csv_results_path):
    """"""

    with open(csv_results_path, "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Start_X", "Start_Y", "End_X", "End_Y", "Dijkstra_sp", "Dijkstra_duration", "Astar_sp", "Astar_duration"])


        start_points = gpd.read_file(output_folder + "start_nodes.gpkg", layer="start_points")
        end_points = gpd.read_file(output_folder + "end_nodes.gpkg", layer="end_points")

        for i in range(0,len(start_points)):
            start = (start_points.loc[i, "geometry"].y, start_points.loc[i, "geometry"].x)
            end = (end_points.loc[i, "geometry"].y, end_points.loc[i, "geometry"].x)

            dijkstra_path = output_optimization_folder + f"sp_dijkstra/dijkstra_{i}.gpkg"
            astar_path = output_optimization_folder + f"sp_alpha_star/astar_{i}.gpkg"


            print(f"Astar {i}")
            stime_astar = time.time()
            # TODO : test manhattan distance
            sp(graph_path = graph_path, start=start, end=end, shortest_path_file_path=astar_path, algorithm="Alpha_star", heuristic=None, weight="IF")
            etime_astar = time.time()
            
            astar_duration = (etime_astar - stime_astar) / 60

            print(f"Dijstra {i}")
            stime_dijkstra = time.time()
            sp(graph_path = graph_path, start=start, end=end, shortest_path_file_path=dijkstra_path, algorithm="Dijkstra", weight="IF")
            etime_dijkstra = time.time()

            dijstra_duration = (etime_dijkstra - stime_dijkstra) / 60


            writer.writerow([start[1], start[0], end[1], end[0], dijkstra_path, dijstra_duration, astar_path, astar_duration])
        

optimization(metrop_graph_path, csv_results_path)