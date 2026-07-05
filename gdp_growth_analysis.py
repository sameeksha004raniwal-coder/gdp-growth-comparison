import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# World Bank indicator for GDP growth annual %
indicator = "NY.GDP.MKTP.KD.ZG"

# Country codes: India = IND, China = CHN, United States = USA
countries = "IND;CHN;USA"

url = f"https://api.worldbank.org/v2/country/{countries}/indicator/{indicator}?format=json&per_page=2000"

response = requests.get(url)
data = response.json()[1]

# Convert JSON data into DataFrame
df = pd.DataFrame(data)

# Keep useful columns
df = df[["country", "countryiso3code", "date", "value"]]

# Clean country names
df["country"] = df["country"].apply(lambda x: x["value"])

# Rename columns
df = df.rename(columns={
    "country": "Country",
    "countryiso3code": "Code",
    "date": "Year",
    "value": "GDP_Growth"
})

# Convert year to integer
df["Year"] = df["Year"].astype(int)

# Drop missing values
df = df.dropna()

# Sort data
df = df.sort_values(by=["Country", "Year"])

# Show first few rows
df.head()

plt.figure(figsize=(12, 6))

sns.lineplot(
    data=df,
    x="Year",
    y="GDP_Growth",
    hue="Country",
    marker="o"
)

plt.title("GDP Growth Comparison: India, China and the United States")
plt.xlabel("Year")
plt.ylabel("GDP Growth (annual %)")
plt.axhline(0, color="black", linewidth=0.8, linestyle="--")
plt.grid(True, alpha=0.3)
plt.legend(title="Country")
plt.show()

summary = df.groupby("Country")["GDP_Growth"].agg(
    Average_Growth="mean",
    Highest_Growth="max",
    Lowest_Growth="min",
    Volatility="std"
).round(2)

summary

# Create time periods
def classify_period(year):
    if year < 2000:
        return "Before 2000"
    elif year <= 2008:
        return "2000-2008"
    elif year <= 2019:
        return "2009-2019"
    else:
        return "2020 onwards"

df["Period"] = df["Year"].apply(classify_period)

period_summary = df.groupby(["Country", "Period"])["GDP_Growth"].mean().round(2).reset_index()

period_summary