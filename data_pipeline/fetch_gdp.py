import requests
import pandas as pd

url = "https://api.worldbank.org/v2/country/all/indicator/NY.GDP.MKTP.CD?format=json"

response = requests.get(url)
data = response.json()

records = []

for item in data[1]:
    records.append({
        "country": item["country"]["value"],
        "year": item["date"],
        "gdp": item["value"]
    })

df = pd.DataFrame(records)

df.to_csv("data/gdp_data.csv", index=False)

print("GDP data fetched successfully!")