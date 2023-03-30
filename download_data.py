import os
from data_utils import download_data, convert_all_gml, create_folder,convert_all_points_into_polygons, write_all_atributes
#from data_informations import services, data_wfs
import geopandas as gpd

# print("#### LOADING ALL DATA #### \n \n")
# create_folder("./data/gml")
# download_data("data.grandlyon_wfs", "2.0.0", "./data/gml")

# print("#### Converting GML into Shapefile #### \n \n")
# create_folder("./data/gpkg")
# convert_all_gml("./data/gpkg/")

# print("#### Converting Points Shapefile into Polygons #### \n \n")
# create_folder("./data/gpkg_buffered")
# convert_all_points_into_polygons("./data/gpkg_buffered/")

write_all_atributes()

# ### Attributes to remove or to add

fontaines_potables = ['gml_id', 'nom', 'gestionnaire', 'anneepose', 'gid', 'geometry']
toilettes_publiques = ['gml_id', 'commune', 'voie', 'numerodansvoie', 'gestionnaire', 'observation', 'identifiant', 'gid', 'geometry']
fontaines_ornementales = ['gml_id', 'nom', 'address', 'commune', 'insee', 'source', 'gid', 'geometry']
parcs_jardins_metropole = ['gml_id', 'uid', 'nom', 'num', 'voie', 'codepost', 'commune', 'code_insee', 'surf_tot_m2', 'gestion', 'clos', 'acces', 'label', 'type_equip', 'eau', 'toilettes', 'chien', 'esp_can', 'gid', 'openinghours', 'timePosition', 'numvoie', 'precision_horaires', 'reglement', 'ann_ouvert', 'circulation', 'photo', 'id_ariane', 'horaires', 'openinghoursspecification', 'geometry']
bancs = ['gml_id', 'materiau', 'dossier', 'insee', 'source', 'gid', 'geometry']
arbres_alignement = ['gml_id', 'essencefrancais', 'circonference_cm', 'hauteurtotale_m', 'hauteurfut_m', 'diametrecouronne_m', 'rayoncouronne_m', 'timePosition', 'genre', 'espece', 'variete', 'essence', 'architecture', 'localisation', 'naturerevetement', 'mobilierurbain', 'anneeplantation', 'commune', 'codeinsee', 'nomvoie', 'codefuv', 'identifiant', 'numero', 'codegenre', 'gid', 'surfacecadre_m2', 'geometry']
