from sklearn.cluster import AgglomerativeClustering

def run_hierarchical(df, k=5):
    X = df[["latitude_scaled", "longitude_scaled"]]

    model = AgglomerativeClustering(n_clusters=k)
    df["cluster_label"] = model.fit_predict(X)

    return df