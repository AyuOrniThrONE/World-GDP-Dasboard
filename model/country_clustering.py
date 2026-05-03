import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import numpy as np

def cluster_countries(df):
    latest_year = df['year'].max()
    df_latest = df[df['year']==latest_year].copy()

    features=df_latest[['gdp_growth','gdp_rolling_avg','cumulative_growth']].fillna(0)

    #Scale features 
    scaler = StandardScaler()
    scaled_features=scaler.fit_transform(features)

    #Apply KMeans
    kmeans=KMeans(n_clusters=3,random_state=42)
    clusters = kmeans.fit_predict(scaled_features)
    df_latest["clusters"] = clusters

    # Dynamically determine cluster labels based on centroids
    # Centroids correspond to the features: gdp_growth, gdp_rolling_avg, cumulative_growth
    centroids = kmeans.cluster_centers_
    
    # We will rank the clusters primarily based on their gdp_growth centroid (index 0)
    gdp_growth_centroids = centroids[:, 0]
    
    # Sort indices to get the mapping from cluster index to rank
    sorted_cluster_indices = np.argsort(gdp_growth_centroids)
    
    struggling_cluster = sorted_cluster_indices[0]
    stable_cluster = sorted_cluster_indices[1]
    high_growth_cluster = sorted_cluster_indices[2]

    cluster_mapping = {
        high_growth_cluster: "High Growth Economies 🚀",
        stable_cluster: "Stable Economies 📊",
        struggling_cluster: "Struggling Economies ⚠️"
    }

    df_latest["cluster_label"] = df_latest["clusters"].map(cluster_mapping)

    return df_latest