import pandas as pd

def clean_gdp_data(input_file="data/gdp_raw.csv", output_file="data/gdp_clean.csv"):
    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"Warning: {input_file} not found. Attempting to use data/gdp_data.csv")
        df = pd.read_csv("data/gdp_data.csv")
        # Keep only the raw columns if we're falling back to the processed dataset
        if "gdp_growth" in df.columns:
            df = df[["country", "year", "gdp_growth"]]

    # Drop missing GDP growth values instead of filling with 0
    df = df.dropna(subset=["gdp_growth"])

    df["year"] = df["year"].astype(int)
    df = df.sort_values(["country", "year"])
    
    df.to_csv(output_file, index=False)
    print("Data cleaned!")

if __name__ == "__main__":
    clean_gdp_data()