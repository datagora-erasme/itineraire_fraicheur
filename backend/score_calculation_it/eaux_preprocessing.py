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

###### EAUX PREPROCESSING ######
"""Les données proviennent de deux sources : plan d'eau importants et plan d'eaux détails de datagranlyon"""

### CREATE WORKING DIRECTORY ###
create_folder("./output_data/eaux/")

### FUNCTION ###

### GLOBAL VARIABLES ###

eaux_details_path = "./input_data/eaux/eaux_details.gpkg"
eaux_importants_path = "./input_data/eaux/eaux_importants.gpkg"

eaux_path = "./output_data/eaux/eaux.gpkg"
eaux_buffer_path = "./output_data/eaux/eaux_buffered.gpkg"

edges_buffer_path = "./input_data/network/edges_buffered_12_bounding.gpkg"
edges_buffer_eaux_prop_path = "./output_data/network/edges/edges_buffered_eaux_prop_bounding.gpkg"

### SCRIPT ###

# eaux_details = gpd.read_file(eaux_details_path)
# eaux_importants = gpd.read_file(eaux_importants_path)

# eaux_details = eaux_details.to_crs(3946)
# eaux_importants = eaux_importants.to_crs(3946)

# eaux_details["class"] = "detail"
# eaux_importants["class"] = "important"

# # Données à retravailler pour un choix non arbitraire
# eaux_details["buffer_size"] = 10
# eaux_importants["buffer_size"] = 50

# eaux = pd.concat([eaux_details, eaux_importants])

# eaux.to_file(eaux_path, driver="GPKG", layer="eaux")

bufferize_with_column(eaux_path, eaux_buffer_path, "eaux", "buffer_size", 5)

calculate_area_proportion(edges_buffer_path, eaux_buffer_path, "eaux", edges_buffer_eaux_prop_path, "edges")