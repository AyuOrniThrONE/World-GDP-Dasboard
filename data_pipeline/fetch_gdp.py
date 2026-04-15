import requests
import pandas as pd

url = "https://data360api.worldbank.org/data360/data?DATABASE_ID=WB_WDI&INDICATOR=WB_WDI_NY_GDP_MKTP_KD_ZG"

response = requests.get(url)
data = response.json()

all_records = []

while url:
    response = requests.get(url)
    data = response.json()

    # Extract records
    records = data.get("value", [])

    for item in records:
        all_records.append({
            "country": item.get("REF_AREA"),
            "year": item.get("TIME_PERIOD"),
            "gdp_growth": item.get("OBS_VALUE")
        })

    # Move to next page
    url = data.get("nextPage")  # automatically handles pagination


df = pd.DataFrame(all_records)

df.to_csv("data/gdp_data.csv", index=False)

print("GDP data fetched successfully!")