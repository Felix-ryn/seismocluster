from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import traceback
import os
from dotenv import load_dotenv

from app.config.database import get_db
from app.models.pipeline import SeismoPipeline

load_dotenv()

router = APIRouter(
    prefix="/api/v1/ml",
    tags=["Machine Learning Operations"]
)

# Lazy init: pipeline dibuat saat request masuk, bukan saat startup
_pipeline: SeismoPipeline = None


def get_pipeline() -> SeismoPipeline:
    global _pipeline
    if _pipeline is None:
        _pipeline = SeismoPipeline()
    return _pipeline


@router.get("/predict-earthquakes")
def predict_earthquakes_endpoint(
    limit: int = Query(default=100, ge=1, le=1000, description="Jumlah prediksi yang dikembalikan"),
    db: Session = Depends(get_db)
):
    """Prediksi real-time menggunakan model lokal joblib."""
    try:
        print("=" * 50)
        print("Menerima request prediksi gempa")

        pipeline = get_pipeline()

        print("STEP 1 - Load data")
        df_raw = pipeline.load_from_db(db)

        if df_raw.empty:
            raise HTTPException(status_code=404, detail="Data gempa kosong")

        print(f"Jumlah data: {len(df_raw)}")

        print("STEP 2 - Preprocessing")
        df_processed = pipeline.prepare_features(df_raw, is_training=False)

        print("STEP 3 - Prediction")
        df_result = pipeline.predict_all(df_processed)

        df_result = df_result.head(limit)

        cols_to_return = [
            'id', 'time', 'latitude', 'longitude',
            'depth', 'magnitude', 'place',
            'zona_klaster', 'is_anomaly'
        ]

        result_json = df_result[cols_to_return].to_dict(orient="records")

        print("Response berhasil dibuat")
        print("=" * 50)

        return {
            "status": "success",
            "message": "Prediksi berhasil",
            "total_data": len(result_json),
            "anomaly_count": int(df_result['is_anomaly'].sum()),
            "data": result_json
        }

    except FileNotFoundError as e:
        print("ERROR SCALER")
        raise HTTPException(
            status_code=400,
            detail=f"Scaler belum tersedia. Jalankan POST /api/v1/clusters/train terlebih dahulu. Detail: {str(e)}"
        )

    except Exception as e:
        print("=" * 50)
        print("ERROR ML PIPELINE")
        print(str(e))
        traceback.print_exc()
        print("=" * 50)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/models")
def get_model_status():
    """Cek status model-model yang tersimpan di local joblib."""
    try:
        models_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../../app/saved_models")
        )

        model_files = {
            "SeismoCluster_Clustering_Model_KMeans": "kmeans_model.joblib",
            "SeismoCluster_Hotspot_Model": "hotspot_model.joblib",
            "SeismoCluster_Anomaly_Model_ISF": "IsoForest_model.joblib",
            "SeismoCluster_Hierarchy_Model": "hierarchy_model.joblib",
        }

        models_info = []

        for model_name, filename in model_files.items():
            filepath = os.path.join(models_dir, filename)
            if os.path.exists(filepath):
                size_mb = round(os.path.getsize(filepath) / (1024 * 1024), 2)
                models_info.append({
                    "name": model_name,
                    "status": "available",
                    "source": "local_joblib",
                    "file": filename,
                    "size_mb": size_mb,
                })
            else:
                models_info.append({
                    "name": model_name,
                    "status": "not_found",
                    "error": f"File {filename} tidak ditemukan di saved_models"
                })

        return {
            "status": "success",
            "source": "local_joblib",
            "models_dir": models_dir,
            "models": models_info
        }

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))