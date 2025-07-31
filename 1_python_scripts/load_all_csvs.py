import os
import pandas as pd

#PATH to the CSV File Directory
base_path = "D:\IoMT-Simulation"

#Store All Datasets
all_dataframes = {}

#Loop Through and Read Each CSV File
for part in ["sim_datapart1", "sim_datapart2", "sim_datapart3", "sim_datapart4"]:
    part_path = os.path.join(base_path, part)
    for filename in os.listdir(part_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(part_path, filename)
            df = pd.read_csv(file_path)
            all_dataframes[filename] = df 

print(f"Loaded {len(all_dataframes)} environment files.")