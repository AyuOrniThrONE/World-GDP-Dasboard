import pandas as pd

df = pd.read_csv("data/gdp_data.csv")

# 1. Year over Year Growth Change
df['growth_change']=df.groupby("country")["gdp_growth"].diff()

# 2. Rolling average (3 year Smoothing)
df["gdp_rolling_avg"]=df.groupby("country")["gdp_growth"].transform(
    lambda x:x.rolling(window=3, min_periods=1).mean()
)

# 3. Cumulative Growth (Long-term trend)
df["cumulative_growth"]=df.groupby("country")["gdp_growth"].cumsum()

# 4. Growth Category (Economic Classification)

def categorize_growth(value):
    if value>6:
        return "High Growth"
    elif value>2:
        return "Moderate Growth"
    elif value>0:
        return "Low Growth"
    else:
        return "Negative Growth"

df["growth_category"]=df["gdp_growth"].apply(categorize_growth)

#Save data

df.to_csv("data/gdp_data.csv",index=False)

print("Data Features Added")