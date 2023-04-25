import os
from data_utils import *
from data_calculation import *
#from data_informations import services, data_wfs
from calculate_itinerary_utils import *
import geopandas as gpd
import time


start_time = time.time()

data_folder_path = "./backend/data/"

# print("### CREATION of data_informations.json file ### ")
# create_folder("./backend/data")
# create_data_informations_file()

# print("#### LOADING ALL DATA #### \n \n")
# create_folder(data_folder_path + "gml")
# download_data_wfs("data.grandlyon_wfs", "2.0.0", data_folder_path + "gml")

# create_folder(data_folder_path + "raster")
# download_data_wms("data.grandlyon_wms", "1.1.1", data_folder_path + "raster")

# print("#### Converting Files #### \n \n")

# create_folder(data_folder_path + "gpkg")
# print("From gml to gpkg \n")
# convert_all(data_folder_path + "gpkg/", input_extension="gml", output_extension="gpkg", driver="GPKG")

# print("From gpkg to geojson \n")
# create_folder(data_folder_path + "geojson")
# convert_all(data_folder_path + "geojson/", input_extension="gpkg", output_extension="json", driver="GeoJSON")
# convert_all(data_folder_path + "geojson/", input_extension="gpkg", output_extension="json", driver="GeoJSON", connection_type="raw")


# write_all_atributes()

# ### Attributes to remove or to add

# ## Remove
# fontaines_potables_rm = ['nom', 'gestionnaire', 'anneepose']
# toilettes_publiques_rm = ['commune', 'voie', 'numerodansvoie', 'gestionnaire', 'observation', 'identifiant']
# fontaines_ornementales_rm = ['nom', 'address', 'commune', 'insee', 'source']
# parcs_jardins_metropole_rm = ['nom', 'num', 'voie', 'codepost', 'commune', 'code_insee', 'surf_tot_m2', 'gestion', 'clos', 'acces', 'label', 'type_equip', 'eau', 'toilettes', 'chien', 'esp_can', 'openinghours', 'timePosition', 'numvoie', 'precision_horaires', 'reglement', 'ann_ouvert', 'circulation', 'photo', 'id_ariane', 'horaires', 'openinghoursspecification']
# bancs_rm = ['dossier', 'insee', 'source']
# #arbres_alignement_rm = ['timePosition','architecture', 'naturerevetement', 'mobilierurbain', 'commune', 'codeinsee', 'nomvoie', 'codefuv', 'identifiant', 'numero']
# ## Add 
# #IF = Indicateur Fraicheur
# fontaines_potables_add = {
#     "data_type": "fontaines_potables",
#     "IF_fontaines_potables" : 140,
#     "buffer_size" : 10
# }
# toilettes_publiques_add = {
#     "data_type": "toilettes_publiques",
#     "IF_toilettes_publiques" : 110,
#     "buffer_size" : 10
# }
# fontaines_ornementales_add = {
#     "data_type": "fontaines_ornementales",
#     "IF_fontaines_ornementales" : 120,
#     "buffer_size" : 10
# }
# parcs_jardins_metropole_add = {
#     "data_type": "parcs_jardins_metropole",
#     "IF_parcs_jardins_metropole" : 130,
#     "buffer_size" : 10
# }
# bancs_add = {
#     "data_type": "bancs",
#     "IF_bancs" : 110,
#     "buffer_size" : 10
# }
# # arbres_alignement_add = {
# #     "data_type": "arbres_alignement",
# #     "IF_arbres_alignement" : 130,
# #     "buffer_size" : 10
# # }

# write_attributes_to_add_and_remove("fontaines_potables", fontaines_potables_add, fontaines_potables_rm)
# write_attributes_to_add_and_remove("toilettes_publiques", toilettes_publiques_add, toilettes_publiques_rm)
# write_attributes_to_add_and_remove("fontaines_ornementales", fontaines_ornementales_add, fontaines_ornementales_rm)
# write_attributes_to_add_and_remove("parcs_jardins_metropole", parcs_jardins_metropole_add, parcs_jardins_metropole_rm)
# write_attributes_to_add_and_remove("bancs", bancs_add, bancs_rm)
# #write_attributes_to_add_and_remove("arbres_alignement", arbres_alignement_add, arbres_alignement_rm)

# create_folder(data_folder_path + "cleaned_data")
# remove_and_add_attributes(data_folder_path + "cleaned_data/")


# print("#### Calculating areas of influence (buffer_size) ####")

# #pca_multiple_imputation("./data/cleaned_data/arbres_alignement_cleaned.gpkg", "rayoncouronne_m")

# #trees_calculate_buffer_size("./data/cleaned_data/arbres_alignement_cleaned.gpkg")

# print("#### Converting Points Shapefile into Polygons #### \n \n")
# create_folder(data_folder_path + "gpkg_buffered")
# convert_all_points_into_polygons(data_folder_path + "gpkg_buffered/")

# print("#### Calculating freshness indicators (IF) #### ")

# print("#### DATA merge #### ")

# merge_data()

print("#### Network OSM extraction ####")
create_folder(data_folder_path +"osm")

# lyon_network_parameters = {
#     "place_name" : "Lyon, France",
#     "network_type" : "walk",
#     "bbox": None,
#     "output_file": data_folder_path+ "osm/lyon_walk_simplified.gpkg"
# }

lyon_network_parameters = {
    "place_name" : "Lyon, France",
    "network_type" : "walk",
    "bbox": (45.954014,45.546274, 5.217133,4.566879),
    "output_file": data_folder_path+ "osm/metrop_walk_simplified.gpkg"
}

load_osm_network(lyon_network_parameters)

print("#### Merge Network and IF layer")

merge_network_data(data_folder_path + "osm/metrop_walk_simplified.gpkg", "./backend/script_python/data/raw_data/joined_if_3946.gpkg", data_folder_path + "osm/weighted_network_walk_metrop_simplified.gpkg")

end_time = time.time()

execution_time = (end_time - start_time)/60
print(f"Temps d'exécution : {execution_time}")