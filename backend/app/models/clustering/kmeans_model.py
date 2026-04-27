from sklearn.cluster import KMeans

def run_kmeans(df, k=5):
    X = df[["latitude_scaled", "longitude_scaled"]]

    model = KMeans(n_clusters=k, random_state=42)
    df["cluster_label"] = model.fit_predict(X)

    return df