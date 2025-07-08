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

room_price.plot(kind="barh", title="Average Price by Room Type") #horizontal bar graph showing price per room type

plt.xlabel("Average Price ($)")
plt.tight_layout()
plt.show()

