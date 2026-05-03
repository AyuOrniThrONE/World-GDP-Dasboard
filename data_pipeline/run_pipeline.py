import sys
import os

# Ensure the data_pipeline directory is in the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fetch_gdp import fetch_data
from clean_data import clean_gdp_data
from feature_engg import engineer_features

def run_all():
    print("Running Data Pipeline...")
    # Step 1: Fetch
    fetch_data("data/gdp_raw.csv")
    
    # Step 2: Clean
    clean_gdp_data("data/gdp_raw.csv", "data/gdp_clean.csv")
    
    # Step 3: Feature Engineering
    engineer_features("data/gdp_clean.csv", "data/gdp_data.csv")
    
    print("Pipeline Complete!")

if __name__ == "__main__":
    run_all()
