from sklearn.ensemble import IsolationForest

def run_isolation(df):
    X = df[["magnitude_scaled", "depth_scaled"]]

    model = IsolationForest(contamination=0.05)
    df["is_anomaly"] = model.fit_predict(X) == -1

    return df