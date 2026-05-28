import mlflow, os, sys
sys.path.insert(0, '.')
from dotenv import load_dotenv
load_dotenv()

mlflow.set_tracking_uri(os.getenv('MLFLOW_TRACKING_URI', 'http://localhost:5000'))
client = mlflow.tracking.MlflowClient()

models = [
    os.getenv('MLFLOW_CLUSTERING_MODEL_NAME', 'SeismoCluster_Clustering_Model_KMeans'),
    os.getenv('MLFLOW_HOTSPOT_MODEL_NAME', 'SeismoCluster_Hotspot_Model'),
    os.getenv('MLFLOW_ANOMALY_MODEL_NAME', 'SeismoCluster_Anomaly_Model_ISF'),
    os.getenv('MLFLOW_HIERARCHY_MODEL_NAME', 'SeismoCluster_Hierarchy_Model'),
]

print("=" * 60)
print("Cek Status Champion Model MLflow")
print("=" * 60)

all_ok = True
for name in models:
    try:
        v = client.get_model_version_by_alias(name, "champion")
        print(f"[OK] {name}")
        print(f"     champion=v{v.version} | run_id={v.run_id[:8]}... | status={v.status}")
    except mlflow.exceptions.MlflowException as e:
        if "RESOURCE_DOES_NOT_EXIST" in str(e) or "not found" in str(e).lower():
            print(f"[!!] {name}: BELUM ADA CHAMPION")
        else:
            print(f"[ERR] {name}: {e}")
        all_ok = False
    except Exception as e:
        print(f"[ERR] {name}: {e}")
        all_ok = False

print("=" * 60)
if all_ok:
    print("Semua model siap digunakan.")
else:
    print("Ada model yang belum punya alias 'champion'.")
    print("Buka MLflow UI -> Models -> pilih model -> klik versi -> tambah alias 'champion'")
print("=" * 60)
