import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from model.gdp_forecast import forecast_country
from model.country_clustering import cluster_countries

# Page config
st.set_page_config(page_title="World GDP Dashboard", layout="wide", page_icon="🌍")

# Custom CSS for Premium Design
st.markdown("""
    <style>
    .main {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 4px 4px 0px 0px;
        gap: 10px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(255, 255, 255, 0.1);
        border-bottom: 2px solid #00E676;
    }
    h1, h2, h3 {
        color: #00E676;
    }
    div[data-testid="stMetricValue"] {
        font-size: 2.5rem;
        color: #00E676;
    }
    </style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    try:
        return pd.read_csv("data/gdp_data.csv")
    except FileNotFoundError:
        st.error("Data file not found. Please run the data pipeline first.")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.stop()

# Title
st.title("🌍 World GDP Growth Dashboard")
st.markdown("*Analyze global economic trends with advanced analytics and predictive forecasting.*")

st.sidebar.header("⚙️ Controls")

countries = df["country"].unique()
selected_country = st.sidebar.selectbox("Select Country", countries)

year_range = st.sidebar.slider(
    "Select Year Range",
    int(df["year"].min()),
    int(df["year"].max()),
    (int(df["year"].min()), int(df["year"].max()))
)

# Filtering data
filtered_df = df[
    (df["country"] == selected_country) &
    (df["year"] >= year_range[0]) &
    (df["year"] <= year_range[1])
]

# Tabs
tab1, tab2, tab3 = st.tabs(["📈 Historical Trends", "🔮 GDP Forecast", "🌍 Global Clustering"])

with tab1:
    if filtered_df.empty:
        st.warning(f"No data available for {selected_country} in the selected year range.")
    else:
        st.subheader(f"GDP Growth Trend - {selected_country}")
        
        # Metrics
        col1, col2, col3 = st.columns(3)
        latest_gdp = filtered_df["gdp_growth"].iloc[-1]
        avg_gdp = filtered_df["gdp_growth"].mean()
        cum_gdp = filtered_df["cumulative_growth"].iloc[-1]
        
        col1.metric("Latest GDP Growth", f"{round(latest_gdp, 2)}%")
        col2.metric("Average GDP Growth", f"{round(avg_gdp, 2)}%")
        col3.metric("Cumulative Growth", f"{round(cum_gdp, 2)}%")
        
        # Charts
        c1, c2 = st.columns(2)
        with c1:
            fig = px.line(
                filtered_df, x="year", y="gdp_growth",
                title="GDP Growth Over Time",
                template="plotly_dark",
                color_discrete_sequence=["#00E676"]
            )
            st.plotly_chart(fig, use_container_width=True)
            
        with c2:
            fig2 = px.line(
                filtered_df, x="year", y=["gdp_growth", "gdp_rolling_avg"],
                title="Actual vs Rolling Average",
                template="plotly_dark",
                color_discrete_sequence=["#00E676", "#FFEA00"]
            )
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown("---")
        st.subheader("Global Comparisons")
        latest_year = df["year"].max()
        top10 = df[df["year"] == latest_year].sort_values("gdp_growth", ascending=False).head(10)
        bottom10 = df[df["year"] == latest_year].sort_values("gdp_growth").head(10)

        c3, c4 = st.columns(2)
        with c3:
            fig3 = px.bar(top10, x="country", y="gdp_growth", title=f"Top 10 Economies ({latest_year})", template="plotly_dark", color="gdp_growth", color_continuous_scale="Viridis")
            st.plotly_chart(fig3, use_container_width=True)
        with c4:
            fig4 = px.bar(bottom10, x="country", y="gdp_growth", title=f"Lowest GDP Growth ({latest_year})", template="plotly_dark", color="gdp_growth", color_continuous_scale="Reds")
            st.plotly_chart(fig4, use_container_width=True)

        st.markdown("---")
        st.subheader("Global GDP Growth Map")
        years = df["year"].sort_values().unique()
        select_year = st.selectbox("Select Year for Map", years, index=len(years)-1)
        map_df = df[df["year"] == select_year]
        
        fig6 = px.choropleth(
            map_df, locations="country", locationmode="ISO-3", color="gdp_growth",
            title=f"GDP Growth by Country in {select_year}",
            template="plotly_dark", color_continuous_scale="Viridis"
        )
        st.plotly_chart(fig6, use_container_width=True)
        
        # Download
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Selected Data", csv, "gdp_data.csv", "text/csv")

with tab2:
    st.subheader("🔮 GDP Forecast")
    st.markdown("Uses Facebook Prophet to predict future GDP growth based on historical trends.")
    
    forecast_years = st.slider("Years to Predict", 1, 10, 5)
    
    if st.button("Generate Forecast", type="primary"):
        with st.spinner("Training model and forecasting..."):
            forecast, model = forecast_country(df, selected_country, forecast_years)
            
            if forecast is None:
                st.warning(f"Not enough historical data to generate a forecast for {selected_country}. Prophet requires at least 2 data points.")
            else:
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=forecast["ds"], y=forecast["yhat"], mode='lines', name='Forecast', line=dict(color='#00E676')))
                fig.add_trace(go.Scatter(x=forecast["ds"], y=forecast["yhat_upper"], mode='lines', name='Upper Bound', line=dict(dash='dot', color='rgba(0, 230, 118, 0.5)')))
                fig.add_trace(go.Scatter(x=forecast["ds"], y=forecast["yhat_lower"], mode='lines', name='Lower Bound', line=dict(dash='dot', color='rgba(0, 230, 118, 0.5)')))
                fig.update_layout(title=f"GDP Growth Forecast for {selected_country}", template="plotly_dark")
                
                st.plotly_chart(fig, use_container_width=True)
                
                latest_prediction = forecast.tail(1)
                st.info(f"**Insight:** Predicted GDP Growth for {latest_prediction['ds'].dt.year.values[0]}: **{round(latest_prediction['yhat'].values[0], 2)}%**")

with tab3:
    st.subheader("🌍 Country Economic Clustering")
    st.markdown("Groups countries into economic clusters using K-Means clustering based on recent growth patterns.")
    
    with st.spinner("Clustering economies..."):
        cluster_df = cluster_countries(df)
        
        fig_cluster = px.scatter(
            cluster_df, x="gdp_growth", y="cumulative_growth", color="cluster_label",
            hover_name="country", title="Country Economic Clusters",
            template="plotly_dark", size_max=15
        )
        st.plotly_chart(fig_cluster, use_container_width=True)
        
        st.markdown("### 📊 Cluster Distribution")
        cluster_counts = cluster_df["cluster_label"].value_counts().reset_index()
        cluster_counts.columns = ["Cluster", "Count"]
        st.dataframe(cluster_counts, hide_index=True)
