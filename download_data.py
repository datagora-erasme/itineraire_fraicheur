from data_utils import download_data, convert_all_gml_data_to_shapefile, points_to_polygon
#from data_informations import services, data_wfs
import geopandas as gpd

print("#### LOADING ALL DATA #### \n \n")

download_data("data.grandlyon_wfs", "2.0.0", "./data/gml")

print("#### Converting GML into Shapefile #### \n \n")

convert_all_gml_data_to_shapefile("./data/shp/")

# print("#### Converting Points Shapefile into Polygons #### \n \n")


