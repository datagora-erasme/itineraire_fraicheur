import seaborn as sns
import pandas as pd
import numpy as np

temp_edges = pd.read_csv("./output_data/csv/temp_dataset.csv")

sns.kdeplot(np.array(temp_edges["temp_35-40_prop"]), bw=0.5)