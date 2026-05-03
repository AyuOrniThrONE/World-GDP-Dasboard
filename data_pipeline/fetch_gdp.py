import requests
import pandas as pd

def fetch_data(output_file="data/gdp_raw.csv"):
    url = "https://data360api.worldbank.org/data360/data?DATABASE_ID=WB_WDI&INDICATOR=WB_WDI_NY_GDP_MKTP_KD_ZG"
    
    all_records = []
    max_pages = 50 # safety limit
    page_count = 0

    while url and page_count < max_pages:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            break

        records = data.get("value", [])
        
        for item in records:
            all_records.append({
                "country": item.get("REF_AREA"),
                "year": item.get("TIME_PERIOD"),
                "gdp_growth": item.get("OBS_VALUE")
            })

        # Move to next page
        # Note: If nextPage doesn't exist, this will break the loop
        url = data.get("nextPage")
        page_count += 1
        print(f"Fetched page {page_count}...")

    if all_records:
        df = pd.DataFrame(all_records)
        df.to_csv(output_file, index=False)
        print(f"GDP data fetched successfully! ({len(all_records)} records)")
    else:
        print("No data was fetched.")

if __name__ == "__main__":
    fetch_data()