import pandas as pd

df = pd.read_csv("data/gdp_data.csv")

df = df.dropna()

df["year"] = df["year"].astype(int)

df = df.sort_values(["country", "year"])

df.to_csv("data/gdp_data.csv", index=False)

print("Data cleaned!")