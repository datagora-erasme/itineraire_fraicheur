from data_utils import download_data, gml_to_shapefile, points_to_polygon
from data_informations import services, data_wfs
import geopandas as gpd
print("#### LOADING ALL DATA #### \n \n")

download_data(services["data.grandlyon_wfs"], "data.grandlyon_wfs", "2.0.0", data_wfs, "./data/gml")

print("#### Converting GML into Shapefile #### \n \n")

gml_to_shapefile("./data/gml/", "./data/shp/", folder=True)

print("#### Converting Points Shapefile into Polygons #### \n \n")

