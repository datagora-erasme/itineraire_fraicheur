import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
from fancyimpute import IterativeImputer
import numpy as np
from sklearn.metrics import r2_score
import pandas as pd

##### PCA IMPUTATION FOR Nan values ######
"""
    Some columns have missing values such as the rayoncouronne one
    Rather than inputing a default value, this is better to imput values based on the other columns. 
    For example two trees of the same species planted at the same time will have most likely the same rayoncouronne.

"""

def pca_multiple_imputation(file_path, column_to_impute):
    print(f"PCA imputation for {file_path} on column {column_to_impute} ... ")
    # read in data
    data = gpd.read_file(file_path)

    # create a copy of the data for imputation
    impute_data = data.copy()

    # impute missing values with iterative imputation
    imputer = IterativeImputer()
    imputed_data = imputer.fit_transform(impute_data[[column_to_impute]])

    impute_data.loc[:, column_to_impute] = imputed_data

    impute_data.to_file(file_path, driver="GPKG")


##### BUFFERING #####

"""
    I choose to make one function per data for the buffer calculation because I hope we'll find / use more accurate attributes 
    to calculate the influence area such as the "rayoncouronne_m" for the trees.

"""

def trees_calculate_buffer_size(file_path, default_buffer_size = 10, default=False):
    print("Calculating tree buffer size")
    trees = gpd.read_file(file_path)

    if(default):
       trees["buffer_size"] = default_buffer_size
    else:
        #buffer size can be a formula between several fields
        trees["buffer_size"] = trees["rayoncouronne_m"]
        
    trees.to_file(file_path, driver="GPKG")

##### Freshness Indicator #####

