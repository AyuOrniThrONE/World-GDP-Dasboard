import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(page_title="World GDP Dashboard")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("../data/gdp_data.csv")

df = load_data()
# Title
st.title("🌍 World GDP Growth Dashboard")
st.markdown("Analyze global economic trends interactively")

st.sidebar.header("Filters")

countries = df["country"].unique()

selected_country = st.sidebar.selectbox("Select Country", countries)

year_range = st.sidebar.slider(
    "Select Year Range",
    int(df["year"].min()),
    int(df["year"].max()),
    (2000, 2022)
)

filtered_df = df[
    (df["country"] == selected_country) &
    (df["year"] >= year_range[0]) &
    (df["year"] <= year_range[1])
]

st.subheader(f"GDP Growth Trend - {selected_country}")

fig = px.line(
    filtered_df,
    x="year",
    y="gdp_growth",
    title="GDP Growth Over Time"
)

st.plotly_chart(fig)

st.subheader("Trend vs Smoothed Growth")

fig2 = px.line(
    filtered_df,
    x="year",
    y=["gdp_growth", "gdp_rolling_avg"],
    title="Actual vs Rolling Average"
)

st.plotly_chart(fig2)

st.subheader("Top 10 Countries by Latest GDP Growth")

latest_year = df["year"].max()

top10 = df[df["year"] == latest_year].sort_values("gdp_growth", ascending=False).head(10)

fig3 = px.bar(
    top10,
    x="country",
    y="gdp_growth",
    title="Top 10 Economies"
)

st.plotly_chart(fig3)

st.subheader("Bottom 10 Countries (Economic Decline)")

bottom10 = df[df["year"] == latest_year].sort_values("gdp_growth").head(10)

fig4 = px.bar(
    bottom10,
    x="country",
    y="gdp_growth",
    title="Lowest GDP Growth"
)

st.plotly_chart(fig4)

st.subheader("Growth Category Distribution")

category_count = df["growth_category"].value_counts()

fig5 = px.pie(
    values=category_count.values,
    names=category_count.index,
    title="Global Growth Categories"
)

st.plotly_chart(fig5)

st.subheader("Global GDP Growth Map")

years = df["year"].sort_values().unique()
select_year = st.selectbox("Select Year", years)

map_df = df[df["year"] == select_year]

fig6 = px.choropleth(
    map_df,
    locations="country",
    locationmode="ISO-3",
    color="gdp_growth",
    title=f"GDP Growth by Country in {select_year}",
    color_continuous_scale="Viridis"
)

st.plotly_chart(fig6)
st.markdown("""
### 📊 Insights
- Compare GDP growth across countries  
- Identify high-growth economies  
- Analyze long-term economic trends  
""")

st.markdown("""
### 📊 Advanced Analytics 
""")

selected_countries = st.sidebar.multiselect("Compare Countries", countries)

compare_df = df[df["country"].isin(selected_countries)]

fig7=px.line(compare_df, x="year", y="gdp_growth", color="country",title=f"Multi-Country Comparison")
st.plotly_chart(fig7)

st.metric("Latest GDP Growth", round(filtered_df["gdp_growth"].iloc[-1], 2),border=True)

st.download_button(
    "Download Data",
    filtered_df.to_csv(index=False),
    "gdp_data.csv"
)