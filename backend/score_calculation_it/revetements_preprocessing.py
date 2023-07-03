import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
import random
import pandas as pd
import multiprocessing as mp
import numpy as np
from shapely.wkt import loads, dumps
import os
import time

# chaussee = gpd.read_file("./chaussee/chaussee.shp")

# chaussee.to_file("./chaussee/chaussee.gpkg", driver="GPKG", layer="chaussee")

chaussee = gpd.read_file("./chaussee/chaussee.gpkg")
print(chaussee.columns)

revetements = chaussee['revetement']

# print(revetements.unique().tolist())
# print(len(revetements))
# print(revetements.isna().sum())

differences_droit_gauche = chaussee[chaussee["reveteme_1"] != chaussee["reveteme_2"]]
print(len(differences_droit_gauche))
print(len(chaussee))

print((len(differences_droit_gauche)/len(chaussee))*100)

# 90 % de béton bitumeux ou d'asphalte => la même chose partout + donnée pas complète sur l'ensemble de la métropole => étude couteuse en temps
# pour un gain moindre. 
