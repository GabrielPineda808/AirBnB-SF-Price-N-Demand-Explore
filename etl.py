import pandas as pd
import argparse

def get_args():
    parser = argparse.ArgumentParser(description="Run Airbnb ETL pipeline.")
    parser.add_argument("--input", default="data/raw-data/listings.csv", help="Path to input CSV file.") #asking for raw data input file path in CLI
    parser.add_argument("--output", default="data/cleaned-data/listings_cleaned.csv", help="Path to save cleaned CSV file.")#asking for cleaned data output fiel path in CLI
    return parser.parse_args()

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

def save_data(df,file_path):
    print(f"Saving clean data into {file_path}...")
    df.to_csv(file_path, index=False)
    print(f"Saved cleaned data into {file_path}.")

def run_etl(input_path, output_path):

    df_raw = load_data(input_path) #loading data to df
    df_cleaned = clean_data(df_raw) #cleaning data
    save_data(df_cleaned, output_path) #writing to csv

if __name__ == "__main__":
    args = get_args()
    run_etl(args.input, args.output)














