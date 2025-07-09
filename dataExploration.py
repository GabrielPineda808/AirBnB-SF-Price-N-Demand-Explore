import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#Load cleaned data into pandas df
df = pd.read_csv("data/cleaned-data/listings_cleaned.csv")

#Price distribution to analyze how prices are set and vary among listings
plt.figure(figsize=(8,4)) #creating new empty figure to plot on

sns.histplot(df['price'], bins= 50, kde=True) #histrogram of price divided into 50 bars with kde line to show the curve

plt.title("Price Distribution") #adding title to plot figure

#adding vertical and horizontal labels to plot figure
plt.xlabel("Price ($)")
plt.ylabel("Count")
plt.show()

#Average Price by Room Type

room_price =df.groupby("room_type")["price"].mean().sort_values() #grabbing the average grouped by room and sorted by price ascending

room_price.plot(kind="barh", title="Average Price by Room Type") #horizontal bar graph showing  average price per room type

plt.xlabel("Average Price ($)")
plt.tight_layout()
plt.show()

#Price by Neighbourhood

plt.figure(figsize=(12,6)) #creating empty plot figure

top_neighbourhoods = df["neighbourhood_cleansed"].value_counts().nlargest(10).index #top 10 neighbourhoods with the most listings

filtered_df = df[df["neighbourhood_cleansed"].isin(top_neighbourhoods)] #new df that only contains data of the top 10 neighbourhood by listings

sns.boxplot(x="neighbourhood_cleansed", y="price", data=filtered_df) #boxplot

plt.title("Price Distribution by Neighborhood (Top 10)")
plt.xlabel("Neighborhood")
plt.ylabel("Price ($)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#Avaliablity vs price

plt.figure(figsize=(8,5))

sns.scatterplot(data=df, x="availability_365", y="price", alpha=0.3)

plt.title("Availability vs. Price")
plt.xlabel("Availability (days/year)")
plt.ylabel("Price ($)")
plt.tight_layout()
plt.show()

#luxury listings per neighborhood

luxury_counts = df[df["luxury_flag"]].groupby("neighbourhood_cleansed")["id"].count().sort_values(ascending=False).head(10)

plt.figure(figsize=(10, 5))
luxury_counts.plot(kind="bar")
plt.title("Top 10 Neighborhoods with Luxury Listings (Price > $500)")
plt.ylabel("Number of Listings")
plt.xlabel("Neighborhood")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#reviews per month vs

plt.figure(figsize=(8, 5))
sns.scatterplot(data=df, x="reviews_per_month", y="price", alpha=0.4)
plt.title("Reviews per Month vs. Price")
plt.xlabel("Reviews per Month")
plt.ylabel("Price ($)")
plt.tight_layout()
plt.show()

#avg price per person by room type

plt.figure(figsize=(8, 5))
df.groupby("room_type")["price_per_person"].mean().sort_values().plot(kind="bar", title="Price per Person by Room Type") #bar graph showing avg price per person by room type
plt.title("Price per Person by Room Type")
plt.ylabel("Price per Person ($)")
plt.xlabel("Room Type")
plt.tight_layout()
plt.show()
