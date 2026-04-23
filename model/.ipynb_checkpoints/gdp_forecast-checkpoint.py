import pandas as pd
from prophet import Prophet

def forecast_country(df, country, years=5):
    # Filter country data
    country_df = df[df["country"] == country][["year", "gdp_growth"]]

    # Rename for Prophet
    country_df = country_df.rename(columns={
        "year": "ds",
        "gdp_growth": "y"
    })

    # Convert year to datetime
    country_df["ds"] = pd.to_datetime(country_df["ds"], format="%Y")

    # Initialize model
    model = Prophet()
    model.fit(country_df)

    # Create future dataframe
    future = model.make_future_dataframe(periods=years, freq="Y")

    # Predict
    forecast = model.predict(future)

    return forecast, model