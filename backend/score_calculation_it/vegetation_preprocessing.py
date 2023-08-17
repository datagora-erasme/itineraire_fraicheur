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
import sys
sys.path.append("../")
from global_variable import *

s = time.time()
###### CREATE WORKING DIRECTORY FOR VEGETATION #######
create_folder("./output_data/vegetation/")
create_folder("./output_data/vegetation/veget_strat/")
create_folder("./output_data/vegetation/arbres_align/")

###### VEGETATION STRATIFIEE PREPROCESSING ######

### FUNCTION ###
def veget_classification(row):
    if(row["vegetation_class"] == 1):
        return "prairie"
    if(row["vegetation_class"] == 2):
        return "arbuste"
    if(row["vegetation_class"] == 3):
        return "arbre"
    

### SCRIPT ###

dissolving(edges_buffer_path, edges_buffer_disolved_path, "edges")

clip_data(edges_buffer_disolved_path, raw_veget_strat_path, veget_strat_path, 4, "edges")

print("###### VEGETATION STRATIFIEE ###### ")
print("Classification Vegetation stratifiee")
# classification(veget_strat_path, veget_strat_class_folder, veget_classification, "veget_strat")

###### ARBRES D'ALIGNEMENT PREPROCESSING ######

### FUNCTION ###
def arbres_align_classification(row):
    if(row["hauteurtot"] > 1.5):
        return "arbre"
    return "arbuste"

### GLOBAL VARIABLES ###
arbres_align_gpkg_path = "./input_data/arbres/arbres.gpkg"
arbres_align_class_folder = "./output_data/vegetation/arbres_align/"
class_arbres_align_path = "./output_data/vegetation/arbres_align/arbres_align_arbre.gpkg"
class_arbustes_align_path = "./output_data/vegetation/arbres_align/arbres_align_arbuste.gpkg"

arbres_align_buffer_path = "./output_data/vegetation/arbres_align/class_arbres_align_buffer_2.gpkg"
arbustes_align_buffer_path = "./output_data/vegetation/arbres_align/class_arbustes_align_buffer_2.gpkg"

clipped_arbres_align_path = "./output_data/vegetation/arbres_align/clipped_arbres_align.gpkg"
clipped_arbustes_align_path = "./output_data/vegetation/arbres_align/clipped_arbustes_align.gpkg"

print("###### ARBRES D'ALIGNEMENT ###### ")

print("Classification arbres alignement")
# classification(arbres_align_gpkg_path, arbres_align_class_folder, arbres_align_classification, "arbres_align")

print("Buffering arbres and arbustes align")
# bufferize_with_column(class_arbres_align_path, arbres_align_buffer_path, "arbres_align_arbre", "rayoncouro", 2.5, coeff_buffer=2)
# bufferize_with_column(class_arbustes_align_path, arbustes_align_buffer_path, "arbres_align_arbuste", "rayoncouro", 2.5, coeff_buffer=2)

# arbres_align_buffer = gpd.read_file(arbres_align_buffer_path)
# arbustes_align_buffer = gpd.read_file(arbustes_align_buffer_path)

# edges_buffer = gpd.read_file(edges_buffer_path)
print("Clipping arbres and arbustes align")
# clip_data(edges_buffer_path, arbres_align_buffer_path, clipped_arbres_align_path, 5, "arbres_align")
# clip_data(edges_buffer_path, arbustes_align_buffer_path, clipped_arbustes_align_path, 5, "arbustes_align")

###### MERGE ARBRES ALIGNEMENT ET VEGETATION STRATIFIEE ###### 

### GLOBAL VARIABLE ###
arbres_align_veget_diff_path = "./output_data/vegetation/arbres_align/diff_arbres_align_veget_2.gpkg"
arbustes_align_veget_diff_path = "./output_data/vegetation/arbres_align/diff_arbustes_align_veget_2.gpkg"

merged_veget_align_arbres_path = "./output_data/vegetation/merged_veget_align_arbres_2.gpkg"
merged_veget_align_arbustes_path = "./output_data/vegetation/merged_veget_align_arbustes_2.gpkg"

print("###### MERGE ARBRES ALIGNEMENT ET VEGETATION STRATIFIEE ###### ")

print("Difference Arbres align Arbres veget")

# clipped_arbres_align = gpd.read_file(clipped_arbres_align_path)
# clipped_arbustes_align = gpd.read_file(clipped_arbustes_align_path)
# clipped_arbres_align = gpd.read_file(arbres_align_buffer_path)
# clipped_arbustes_align = gpd.read_file(arbustes_align_buffer_path)

# clipped_veget_arbres = gpd.read_file(clipped_arbres_veget_strat_path)
# clipped_veget_arbustes = gpd.read_file(clipped_arbustes_veget_strat_path)

# print("difference arbre align")
# arbres_align_diff = gpd.overlay(arbres_align_buffer, clipped_veget_arbres, how="difference", keep_geom_type=False)
# arbres_align_diff.to_file(arbres_align_veget_diff_path, driver="GPKG", layer="arbres_align")

# print("difference arbustes align")
# arbustes_align_diff = gpd.overlay(arbustes_align_buffer, clipped_veget_arbustes, how="difference", keep_geom_type=False)
# arbustes_align_diff.to_file(arbustes_align_veget_diff_path, driver="GPKG", layer="arbustes_align")


print("merge layers")
print("arbres")
# arbres_align_diff = gpd.read_file(arbres_align_veget_diff_path)
# veget_arbres = gpd.read_file(clipped_arbres_veget_strat_path)

# arbres_align_diff = arbres_align_diff[["geometry"]]
# arbres_align_diff["vegetation_class"] = 3
# arbres_align_diff["class"] = "arbre"

# veget_align_arbres = pd.concat([arbres_align_diff, veget_arbres])

# veget_align_arbres.to_file(merged_veget_align_arbres_path, driver="GPKG", layer="veget")

# print("arbustes")
# arbustes_align_diff = gpd.read_file(arbustes_align_veget_diff_path)
# veget_arbustes = gpd.read_file(clipped_arbustes_veget_strat_path)

# arbustes_align_diff = arbustes_align_diff[["geometry"]]
# arbustes_align_diff["vegetation_class"] = 3
# arbustes_align_diff["class"] = "arbuste"

# veget_align_arbustes = pd.concat([arbustes_align_diff, veget_arbustes])

# veget_align_arbustes.to_file(merged_veget_align_arbustes_path, driver="GPKG", layer="veget")

###### CALCULATE VEGETATION PROPORTION ON EDGES ######
print("###### CALCULATE VEGETATION PROPORTION ON EDGES ######")

print("Calculate arbres proportion")
calculate_area_proportion(edges_buffer_path, merged_veget_align_arbres_path, "arbres", edges_buffer_arbres_prop_path, "edges")

print("Calculate arbustes proportion")
calculate_area_proportion(edges_buffer_path, merged_veget_align_arbustes_path, "arbustes", edges_buffer_arbustes_prop_path, "edges")
print("Calculate prairie proportion")
calculate_area_proportion(edges_buffer_path, clipped_prairie_veget_strat_path, "prairies", edges_buffer_prairies_prop_path, "edges")

e = time.time()

duration = (e-s)/60

print("Duration Vegetation Preprocessing : ", duration)



