import os
from data_utils import create_data_informations_file, download_data, convert_all_gml, create_folder,convert_all_points_into_polygons, write_all_atributes
#from data_informations import services, data_wfs
import geopandas as gpd

print("### CREATION of data_informations.json file ### ")
create_data_informations_file()

print("#### LOADING ALL DATA #### \n \n")
create_folder("./data/gml")
download_data("data.grandlyon_wfs", "2.0.0", "./data/gml")

print("#### Converting GML into Shapefile #### \n \n")
create_folder("./data/gpkg")
convert_all_gml("./data/gpkg/")

print("#### Converting Points Shapefile into Polygons #### \n \n")
create_folder("./data/gpkg_buffered")
convert_all_points_into_polygons("./data/gpkg_buffered/")

write_all_atributes()

# # ### Attributes to remove or to add

# fontaines_potables_rm = ['gml_id', 'gid', 'geometry']
# toilettes_publiques_rm = ['gml_id', 'gid', 'geometry']
# fontaines_ornementales_rm = ['gml_id', 'gid', 'geometry']
# parcs_jardins_metropole_rm = ['gml_id', 'uid','gid', 'geometry']
# bancs_rm = ['gml_id', 'materiau', 'gid', 'geometry']
# arbres_alignement_rm = ['gml_id', 'essencefrancais', 'circonference_cm', 'hauteurtotale_m', 'diametrecouronne_m', 'rayoncouronne_m', 'genre', 'espece', 'variete', 'essence', 'architecture', 'gid', 'surfacecadre_m2', 'geometry']
