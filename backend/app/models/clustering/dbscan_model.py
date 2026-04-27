from sklearn.cluster import DBSCAN

def run_dbscan(df):
    X = df[["latitude_scaled", "longitude_scaled"]]

    model = DBSCAN(eps=0.5, min_samples=5)
    labels = model.fit_predict(X)

    df["cluster_label"] = labels
    df["is_noise"] = labels == -1

    return df