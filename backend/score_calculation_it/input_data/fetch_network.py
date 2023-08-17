import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
import osmnx as ox
import sys
sys.path.append("../../")
from global_variable import *

network_filters = "[\"highway\"][\"area\"!~\"yes\"][\"highway\"!~\"abandoned|bus_guideway|construction|cycleway|motorway|trunk|planned|platform|proposed|raceway|motorway_link|trunk_link|escape|busway\"][\"foot\"!~\"no\"][\"service\"!~\"private\"][\"sidewalk\"!~\"no\"]"

"""
    The bounding_metrop file contains the bounding of Lyon metropole. It is used to define graph query limit in the
    ox.graph_from_polygon function.
"""

bounding_metrop = gpd.read_file(bounding_metrop_path)

bounding_metrop = bounding_metrop.to_crs("4326")

geometry = bounding_metrop["geometry"].iloc[0]

G = ox.graph_from_polygon(geometry, custom_filter=network_filters)

#EPSG:3946 is the default projection system used by datagrandlyon.
G = ox.project_graph(G, to_crs="EPSG:3946")

ox.save_graph_geopackage(G, metrop_network_bouding_path)

def bufferize(input_path, output_path, layer, buffer_size):
    """Bufferize a layer according to a buffer_size and save the ouput file"""
    layer_gpd = gpd.read_file(input_path, layer=layer)

    layer_gpd = layer_gpd.to_crs(3946)

    buffered_features = layer_gpd.geometry.apply(lambda x: x.buffer(buffer_size))

    layer_buffer = gpd.GeoDataFrame(layer_gpd.drop("geometry", axis=1), geometry=buffered_features)
    layer_buffer.crs = layer_gpd.crs

    layer_buffer.to_file(output_path, driver="GPKG", layer=layer)

bufferize(metrop_network_bouding_path, edges_buffer_path, "edges", 6.25)

