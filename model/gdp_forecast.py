import pandas as pd
from prophet import Prophet
import logging
import warnings

# Suppress Prophet logging
logging.getLogger('cmdstanpy').setLevel(logging.WARNING)
warnings.filterwarnings('ignore')

def forecast_country(df, country, years=5):
    # Filter country data
    country_df = df[df["country"] == country][["year", "gdp_growth"]].dropna()

    if len(country_df) < 2:
        return None, None

    # Rename for Prophet
    country_df = country_df.rename(columns={
        "year": "ds",
        "gdp_growth": "y"
    })

    # Convert year to datetime
    country_df["ds"] = pd.to_datetime(country_df["ds"], format="%Y")

    # Initialize model
    model = Prophet(yearly_seasonality=False, weekly_seasonality=False, daily_seasonality=False)
    
    try:
        model.fit(country_df)
    except Exception as e:
        print(f"Prophet fitting failed: {e}")
        return None, None

    # Create future dataframe
    future = model.make_future_dataframe(periods=years, freq="YE")

    # Predict
    forecast = model.predict(future)

    return forecast, model