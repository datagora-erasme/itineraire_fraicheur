from load_data_utils import load_data
from data_informations import services, data_wfs

print("#### LOADING ALL DATA #### \n \n")

load_data(services["data.grandlyon_wfs"], "data.grandlyon_wfs", "2.0.0", data_wfs, "./data")
