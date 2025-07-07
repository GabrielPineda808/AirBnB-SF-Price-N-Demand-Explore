import pandas as pd
import numpy as np
import os

#Define the data paths
raw_data = os.path.join("..", "data", "raw-data", "listings.csv")
processed_data = os.path.join("..", "data", "cleaned-data", "listings_cleaned.csv")

#load the raw data into a pandas dataframe
def load_data():

    print(f"Loading data from {raw_data}...")

    df = pd.read_csv(raw_data)

    print(f"Loaded {len(df)} rows and {len(df.columns)} columns.")
    return df

