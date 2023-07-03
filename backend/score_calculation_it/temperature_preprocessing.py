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
from data_utils import *

###### CREATE WORKING DIRECTORY FOR TEMPERATURE ######

###### TEMPERATURE PREPROCESSING ######
"""Données issue de calcul QGIS pour estimer la T° de surface à partir d'une capture Landsat"""

### FUNCTION ###

def weighted_temp_average(x):
    return pd.Series({
        "C_wavg": round(np.average(x["C"], weights=x["area"]), 2)
        })

### GLOBAL VARIABLE ###
edges_buffer_path = "./input_data/network/edges_buffered_12_bounding.gpkg"
edges_buffer_temp_wavg_path = "./output_data/network/edges/edges_buffered_temp_wavg_bounding.gpkg"

temperature_path = "./input_data/temperature/temp_0722.gpkg"
    
print("Calculate Temperature weighted average ")
calculate_weighted_average(edges_buffer_path, temperature_path, edges_buffer_temp_wavg_path, "edges", "C", weighted_temp_average)

print("read file")
temp_edges = gpd.read_file(edges_buffer_temp_wavg_path)

print("fill na")
temp_edges["C_wavg"] = temp_edges["C_wavg"].fillna(33)


print("to file")
temp_edges.to_file(edges_buffer_temp_wavg_path)