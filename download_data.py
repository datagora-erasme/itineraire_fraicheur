import os
from data_utils import download_data, convert_all_gml_data_to_shapefile, create_folder,convert_all_points_into_polygons
#from data_informations import services, data_wfs
import geopandas as gpd

print("#### LOADING ALL DATA #### \n \n")
create_folder("./data/gml")
download_data("data.grandlyon_wfs", "2.0.0", "./data/gml")

print("#### Converting GML into Shapefile #### \n \n")
create_folder("./data/shp")
convert_all_gml_data_to_shapefile("./data/shp/")

print("#### Converting Points Shapefile into Polygons #### \n \n")
create_folder("./data/shp_buffered")
convert_all_points_into_polygons("./data/shp_buffered/")

