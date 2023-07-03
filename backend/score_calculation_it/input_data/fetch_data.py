import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
from owslib.wfs import WebFeatureService

###### FETCH DATA FROM DATAGRANDLYON ######
def create_folder(folder_path):
    exist = os.path.exists(folder_path)
    if not exist:
        os.makedirs(folder_path)
        print(f"{folder_path} created")

### CREATE WORKING DIRECTORIES ###
create_folder("input_data/parcs/")
create_folder("./input_data/fontaines/")
create_folder("./input_data/vegetation/")
create_folder("./input_data/toilettes/")
create_folder("./input_data/bancs/")
create_folder("./input_data/eaux/")

### GLOBAL VARIABLE ###
geojsonOutputFormat = "application/json; subtype=geojson"

# PARCS #
parcs_wfs_key = "ms:com_donnees_communales.comparcjardin_1_0_0"
parcs_canop_wfs_key = "ms:evg_esp_veg.evgparcindiccanope_latest"

parcs_canop_path = "./input_data/parcs/parcs_canop"
parcs_path = "./input_data/parcs/parcs"

# FONTAINES #
fontaines_potables_wfs_key = "ms:adr_voie_lieu.adrbornefontaine_latest"
fontaines_ornementales_wfs_key = "ms:adr_voie_lieu.adrfontaineornem_latest"

fontaines_pot_path = "./input_data/fontaines/fontaines_potables"
fontaines_orn_path = "./input_data/fontaines/fontaines_ornementales"

# TOILETTES #
toilettes_wfs_key = "ms:adr_voie_lieu.adrtoilettepublique_latest"
toilettes_path = "./input_data/toilettes/toilettes"

# BANCS #
bancs_wfs_key = "ms:adr_voie_lieu.adrbanc_latest"
bancs_path = "./input_data/bancs/bancs"

# COURS D'EAUX #
eaux_details_wfs_key = "ms:fpc_fond_plan_communaut.fpcplandeaudetail"
eaux_details_path = "./input_data/eaux/eaux_details"

eaux_importants_wfs_key = "ms:fpc_fond_plan_communaut.fpcplandeau"
eaux_importants_path = "./input_data/eaux/eaux_importants"

### FUNCTION ###

def connection_wfs(url, service_name, version):
    """ Return a wfs object after connecting to a service thanks the url provided """
    print(f"Connecting {service_name} WFS ... ")
    wfs=None
    try:
        wfs = WebFeatureService(url, version)
        print(f"SUCCESS : Connected to {service_name}")
    except NameError:
        print(f"Error while connecting to {service_name} ... : {NameError}")

    return wfs

def download_data(wfs, data_key, outputFormat, output_path, layername):
    bbox = wfs.contents[data_key].boundingBoxWGS84
    try:
        data = wfs.getfeature(typename=data_key, bbox=bbox, outputFormat=outputFormat)
        print(f"{data_key} fetched with sucess")
    except NameError:
        print(f"Error fetching {data_key}")

    file = open(f"{output_path}.json", "wb")
    file.write(data.read())
    file.close()

    data_gpd = gpd.read_file(f"{output_path}.json")

    #crs : 3946 more accurate crs for Lyon metropole
    data_gpkg = data_gpd.to_crs(3946)
    data_gpkg.to_file(f"{output_path}.gpkg", driver="GPKG", layer=layername)

    #crs : 4326 for leaflet
    data_geojson = data_gpd.to_crs(4326)
    data_geojson.to_file(f"{output_path}.json", driver="GeoJSON")
    

### SCRIPT ###

## WFS CONNECTION ##
print("WFS CONNECTION")
data_grandlyon_wfs_url = "https://download.data.grandlyon.com/wfs/grandlyon?SERVICE=WFS&VERSION=2.0.0"
data_grandlyon_wfs = connection_wfs(data_grandlyon_wfs_url, "datagrandlyon", "2.0.0")

## DATA DOWNLOAD ##
print("Data Download")

print("Parcs")
# download_data(data_grandlyon_wfs, parcs_canop_wfs_key, geojsonOutputFormat, parcs_canop_path, "parcs")
# download_data(data_grandlyon_wfs, parcs_wfs_key, geojsonOutputFormat, parcs_path, "parcs")

print("Fontaines")  
download_data(data_grandlyon_wfs, fontaines_potables_wfs_key, geojsonOutputFormat, fontaines_pot_path, "fontaines_potables")
download_data(data_grandlyon_wfs, fontaines_ornementales_wfs_key, geojsonOutputFormat, fontaines_orn_path, "fontaines_ornementales")

print("Toilettes")
# download_data(data_grandlyon_wfs, toilettes_wfs_key, geojsonOutputFormat, toilettes_path, "toilettes")

print("Bancs")
# download_data(data_grandlyon_wfs, bancs_wfs_key, geojsonOutputFormat, bancs_path, "bancs")

print("Cours d'eau")
# download_data(data_grandlyon_wfs, eaux_details_wfs_key, geojsonOutputFormat, eaux_details_path, "eaux")
# download_data(data_grandlyon_wfs, eaux_importants_wfs_key, geojsonOutputFormat, eaux_importants_path, "eaux")