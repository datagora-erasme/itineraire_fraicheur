import os
from data_utils import download_data, convert_all_gml_data_to_shapefile, create_folder,convert_all_points_into_polygons, write_all_atributes
#from data_informations import services, data_wfs
import geopandas as gpd

# print("#### LOADING ALL DATA #### \n \n")
# create_folder("./data/gml")
# download_data("data.grandlyon_wfs", "2.0.0", "./data/gml")

print("#### Converting GML into Shapefile #### \n \n")
create_folder("./data/shp")
convert_all_gml_data_to_shapefile("./data/shp/")

# print("#### Converting Points Shapefile into Polygons #### \n \n")
# create_folder("./data/shp_buffered")
# convert_all_points_into_polygons("./data/shp_buffered/")

# write_all_atributes()

# ### Attributes to remove or to add

# fontaines_potables_rm  = ['gml_id', 'nom', 'gestionnai', 'anneepose', 'gid', 'geometry']
# toilettes_publiques_rm = ['gml_id', 'commune', 'voie', 'numerodans', 'gestionnai', 'observatio', 'identifian', 'gid', 'geometry']
# fontaines_ornementales_rm = ['gml_id', 'nom', 'address', 'commune', 'insee', 'source', 'gid', 'geometry']
# parcs_jardins_metropole_rm = ['gml_id', 'uid', 'nom', 'num', 'voie', 'codepost', 'commune', 'code_insee', 'surf_tot_m', 'gestion', 'clos', 'acces', 'label', 'type_equip', 'eau', 'toilettes', 'chien', 'esp_can', 'gid', 'openinghou', 'timePositi', 'numvoie', 'precision_', 'reglement', 'ann_ouvert', 'circulatio', 'photo', 'id_ariane', 'horaires', 'openingh_1', 'geometry']
# bancs_rm =  ['gml_id', 'materiau', 'dossier', 'insee', 'source', 'gid', 'geometry']
# arbres_alignement_rm =  ['gml_id', 'essencefra', 'circonfere', 'hauteurtot', 'hauteurfut', 'diametreco', 'rayoncouro', 'timePositi', 'genre', 'espece', 'variete', 'essence', 'architectu', 'localisati', 'naturereve', 'mobilierur', 'anneeplant', 'commune', 'codeinsee', 'nomvoie', 'codefuv', 'identifian', 'numero', 'codegenre', 'gid', 'surfacecad', 'geometry']

