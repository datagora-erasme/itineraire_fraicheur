import geopandas as gpd
import matplotlib.pyplot as plt

## Load data ##

fontaines_potables = gpd.read_file("./data/shp/fontaines_potables.shp")
# print(fontaines_potables.crs)
# print(fontaines_potables['geometry']).head()

## Draw data ##
fontaines_potables.plot()