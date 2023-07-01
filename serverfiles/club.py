import os
import pandas as pd

path_to_csv = os.getcwd()
file_list = [pos_csv for pos_csv in os.listdir(path_to_csv) if pos_csv.endswith('.csv')]

csv_merged = []
 
for file in file_list:
    df = pd.read_csv(file)
    list_dicts = df.to_dict("records")
    csv_merged = csv_merged + list_dicts

df_merged = pd.DataFrame(csv_merged)

df_merged.to_csv("combined.csv")

