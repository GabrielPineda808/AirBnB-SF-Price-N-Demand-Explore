import pandas as pd
import numpy as np
import os

#Define the data paths
raw_data = os.path.join("data", "raw-data", "listings.csv")
processed_data = os.path.join("data", "cleaned-data", "listings_cleaned.csv")

#load the raw data into a pandas dataframe
def load_data(file_path):

    print(f"Loading data from {file_path}...")

    df = pd.read_csv(file_path)

    print(f"Loaded {len(df)} rows and {len(df.columns)} columns.")
    return df

def clean_data(df):
    print("Cleaning data...")

    #keeping columns that are relevant
    relevant_columns = [
        "id", "name", "host_id", "neighbourhood_cleansed", "room_type",
        "price", "minimum_nights", "number_of_reviews", "availability_365",
        "bedrooms", "bathrooms", "review_scores_rating"
    ]

    #reassignging data frame to only contain data from relevant columns
    df = df[relevant_columns]

    #remove rows with missing prices
    df = df[df["price"].notna()]

    #convert price from a string to a float
    df["price"] = (
        df["price"]
        .replace({r"[\$,]"}, '', regex=True) #removes $ symbol and commas in price string
        .astype(float)
    )

    #removing rows with unrealistic price or nights
    df = df[(df["minimum_nights"] <= 30) & (df["price"] < 1000)]

    # fill missing bedrooms or bathrooms with the median
    df["bedrooms"] = df["bedrooms"].fillna(df["bedrooms"].median())
    df["bathrooms"] = df["bathrooms"].fillna(df["bathrooms"].median())

    #create a new column for price per bedroom
    df["price_per_room"] = df["price"] / df["bedrooms"]

    print(f"Cleaned data contains {len(df)} rows and {len(df.columns)} columns.")
    return df

def save_data(df):
    print(f"Saving clean data into {processed_data}...")
    df.to_csv(processed_data, index=False)
    print(f"Saved cleaned data into {processed_data}.")

def run_etl():

    df_raw = load_data(raw_data) #loading data to df
    df_cleaned = clean_data(df_raw) #cleaning data
    save_data(df_cleaned) #writing to csv

run_etl()













