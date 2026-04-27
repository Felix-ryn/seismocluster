from app.models.clustering.dbscan_model import run_dbscan

def run_pipeline(df):
    df = run_dbscan(df)
    return df