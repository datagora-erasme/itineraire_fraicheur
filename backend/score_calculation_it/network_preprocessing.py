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

# network = gpd.read_file("./data/metrop_network.gpkg")

route = gpd.read_file("./chaussee/chaussee.shp")

route.to_csv("./chaussee/chaussee.csv")
