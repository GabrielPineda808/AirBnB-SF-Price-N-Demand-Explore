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

def clean_data(df):
    print(f"Cleaning data from {raw_data}...")

    #keeping columns that are relevant
    columns = [
        "id", "name", "host_id", "neighborhood_cleansed", "room_type",
        "price", "minimum_nights", "number_of_reviews", "availabilitiy_365",
        "bedrooms", "bathrooms", "review_scores_rating"
    ]

    #reassignging data frame to only contain data from relevant columns
    df = df[columns]

    #remove rows with missing prices
    df = df[df["price"].notna()]

    #convert price from a string to a float
    df["price"] = (
        df["price"]
        .replace('[\$,]', '', regex=True) #removes $ symbol and commas in price string
        .astype(float)
    )
