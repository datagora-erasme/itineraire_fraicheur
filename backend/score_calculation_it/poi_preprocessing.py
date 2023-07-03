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

###### POI PREPROCESSING ######

### CREATE WORKING DIRECTORIES ###
create_folder("./output_data/toilettes/")
create_folder("./output_data/fontaines/")
create_folder("./output_data/bancs/")

### GLOBAL FUNCTION ###
def presency(x):
    x_class = x["class"].unique().tolist()
    first_non_one = next((True for val in x_class if val != 1), False)

    return pd.Series({
        "class": first_non_one
    })

### NETWORK VARIABLES ###
edges_buffer_path = "./input_data/network/edges_buffered_12_bounding.gpkg"
edges_buffer_toilette_path = "./output_data/network/edges/edges_buffered_toilette.gpkg"
edges_buffer_fontaines_potables_path = "./output_data/network/edges/edges_buffered_fontaines_potables.gpkg"
edges_buffer_fontaines_ornementales_path = "./output_data/network/edges/edges_buffered_fontaines_ornementales.gpkg"
edges_buffer_bancs_path = "./output_data/network/edges/edges_buffered_bancs.gpkg"

###### TOILETTES ######
### GLOBAL VARIABLES ###
toilette_path = "./input_data/toilettes/toilettes.gpkg"
toilette_buffer_path = "./output_data/toilettes/toilettes_buffered.gpkg"

### SCRIPT ###
print("Toilettes")
# toilette = gpd.read_file(toilette_path)
# toilette["class"] = "toilettes"
# toilette.to_file(toilette_path, driver="GPKG", layer="toilettes")
# bufferize(toilette_path, toilette_buffer_path, "toilettes", 20) #valeur arbitraire de 20mètres pour le moment

calculate_presency(edges_buffer_path, toilette_buffer_path, edges_buffer_toilette_path, "edges", "toilettes", presency)

###### FONTAINES POTABLES ######
### GLOBAL VARIABLES ###
fontaines_potables_path = "./input_data/fontaines/fontaines_potables.gpkg"
fontaines_potables_buffer_path = "./output_data/fontaines/fontaines_potables_buffered.gpkg"

### SCRIPT ###
print("Fontaines potables")
# fontaines_potables = gpd.read_file(fontaines_potables_path)
# fontaines_potables["class"] = "fontaines_potables"
# fontaines_potables.to_file(fontaines_potables_path, driver="GPKG", layer="fontaines_potables")
# bufferize(fontaines_potables_path, fontaines_potables_buffer_path, "fontaines_potables", 30)

calculate_presency(edges_buffer_path, fontaines_potables_buffer_path, edges_buffer_fontaines_potables_path, "edges", "fontaines_potables", presency)


##### FONTAINES ORNEMENTALES ######
### GLOBAL VARIABLES ###
fontaines_ornementales_path = "./input_data/fontaines/fontaines_ornementales.gpkg"
fontaines_ornementales_buffer_path = "./output_data/fontaines/fontaines_ornementales_buffered.gpkg"

### SCRIPT ###
print("Fontaines ornementales")
# fontaines_ornementales = gpd.read_file(fontaines_ornementales_path)
# fontaines_ornementales["class"] = "fontaines_ornementales"
# fontaines_ornementales.to_file(fontaines_ornementales_path, driver="GPKG", layer="fontaines_ornementales")
# bufferize(fontaines_ornementales_path, fontaines_ornementales_buffer_path, "fontaines_ornementales", 25)

calculate_presency(edges_buffer_path, fontaines_ornementales_buffer_path, edges_buffer_fontaines_ornementales_path, "edges", "fontaines_ornementales", presency)

###### BANCS ######
### GLOBAL VARIABLES ###
bancs_path = "./input_data/bancs/bancs.gpkg"
bancs_buffer_path = "./output_data/bancs/bancs_buffered.gpkg"

### SCRIPT ###
print("Bancs")
# bancs = gpd.read_file(bancs_path)
# bancs["class"] = "bancs"
# bancs.to_file(bancs_path, driver="GPKG", layer="bancs")
# bufferize(bancs_path, bancs_buffer_path, "bancs", 10)

#calculate_presency(edges_buffer_path, bancs_buffer_path, edges_buffer_bancs_path, "edges", "bancs", presency)