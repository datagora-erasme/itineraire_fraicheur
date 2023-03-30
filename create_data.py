import os
from data_utils import *
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

### Attributes to remove or to add

## Remove
fontaines_potables_rm = ['nom', 'gestionnaire', 'anneepose']
toilettes_publiques_rm = ['commune', 'voie', 'numerodansvoie', 'gestionnaire', 'observation', 'identifiant']
fontaines_ornementales_rm = ['nom', 'address', 'commune', 'insee', 'source']
parcs_jardins_metropole_rm = ['nom', 'num', 'voie', 'codepost', 'commune', 'code_insee', 'surf_tot_m2', 'gestion', 'clos', 'acces', 'label', 'type_equip', 'eau', 'toilettes', 'chien', 'esp_can', 'openinghours', 'timePosition', 'numvoie', 'precision_horaires', 'reglement', 'ann_ouvert', 'circulation', 'photo', 'id_ariane', 'horaires', 'openinghoursspecification']
bancs_rm = ['dossier', 'insee', 'source']
arbres_alignement_rm = ['timePosition','architecture', 'localisation', 'naturerevetement', 'mobilierurbain', 'anneeplantation', 'commune', 'codeinsee', 'nomvoie', 'codefuv', 'identifiant', 'numero']
## Add 
#IF = Indicateur Fraicheur
fontaines_potables_add = {
    "IF" : 100
}
toilettes_publiques_add = {
    "IF" : 100
}
fontaines_ornementales_add = {
    "IF" : 100
}
parcs_jardins_metropole_add = {
    "IF" : 100
}
bancs_add = {
    "IF" : 100
}
arbres_alignement_add = {
    "IF" : 100
}

write_attributes_to_add_and_remove("fontaines_potables", fontaines_potables_add, fontaines_potables_rm)
write_attributes_to_add_and_remove("toilettes_publiques", toilettes_publiques_add, toilettes_publiques_rm)
write_attributes_to_add_and_remove("fontaines_ornementales", fontaines_ornementales_add, fontaines_ornementales_rm)
write_attributes_to_add_and_remove("parcs_jardins_metropole", parcs_jardins_metropole_add, parcs_jardins_metropole_rm)
write_attributes_to_add_and_remove("bancs", bancs_add, bancs_rm)
write_attributes_to_add_and_remove("arbres_alignement", arbres_alignement_add, arbres_alignement_rm)


create_folder("./data/cleaned_data")
remove_and_add_attributes("./data/cleaned_data/")