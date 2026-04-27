from sklearn.metrics import silhouette_score

def evaluate(df):
    X = df[["latitude_scaled", "longitude_scaled"]]
    labels = df["cluster_label"]

    return {
        "silhouette": silhouette_score(X, labels)
    }