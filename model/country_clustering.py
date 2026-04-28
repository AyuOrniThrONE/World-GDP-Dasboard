import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
def cluster_labels(row):
    if row["clusters"]==0:
        return "Emerging"
    elif row["clusters"]==1:
        return "Developed"
    else:
        return "Struggling"
    


def cluster_countries(df):
    latest_year = df['year'].max()
    df_latest = df[df['year']==latest_year].copy()

    features=df_latest[['gdp_growth','gdp_rolling_avg','cumulative_growth']].fillna(0)

    #Scale features 
    scaler = StandardScaler()
    scaled_features=scaler.fit_transform(features)

    #Apply KMeans
    kmeans=KMeans(n_clusters=3,random_state=42)
    df_latest["clusters"]=kmeans.fit_predict(scaled_features)

    df_latest["cluster_label"]=df_latest.apply(cluster_labels,axis=1)

    return df_latest