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
        "bedrooms", "bathrooms", "review_scores_rating", "accommodates",
        "reviews_per_month", "host_since"
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
    df["price_per_bedroom"] = df["price"] / df["bedrooms"]
    df["price_per_bedroom"] = (
        df["price_per_bedroom"]
        .replace({r"[\$,]"}, '', regex=True) #removes $ symbol and commas in price string
        .astype(float)
    )

    #create a new column for price per bathroom
    df["price_per_bathroom"] = df["price"] / df["bathrooms"]

    #price per person column
    df["price_per_person"] = df["price"] / df["accommodates"]

    #reviews per month column
    df["reviews_per_month"] = df["reviews_per_month"].fillna(0)

    #adding host experience
    df["host_since"] = pd.to_datetime(df["host_since"], errors="coerce")
    df["host_experience_years"] = (pd.Timestamp("now") - df["host_since"]).dt.days / 365
    df["experienced_host"] = df["host_experience_years"] >= 3

    #create a column to flag for luxury listings
    df["luxury_flag"] = df["price"] > 500

    # Check remaining null values
    null_summary = df.isnull().sum()
    print("Missing values: ", null_summary[null_summary > 0])

    # Drop duplicates if any
    df = df.drop_duplicates()
    print("Shape after dropping duplicates:", df.shape)


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














