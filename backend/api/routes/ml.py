from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import json

# Import dependensi
from app.config.database import get_db
from app.models.pipeline import SeismoPipeline


# Membuat router khusus untuk operasi Machine Learning
router = APIRouter(prefix="/api/v1/ml", tags=["Machine Learning Operations"])

# Inisialisasi pipeline secara global di tingkat router
# Ini mencegah pemuatan ulang (reload) model MLflow setiap kali endpoint dipanggil
pipeline = SeismoPipeline()

@router.get("/predict-earthquakes")
def predict_earthquakes_endpoint(db: Session = Depends(get_db)):
    """
    Endpoint Produksi untuk Inferensi MLOps:
    1. Extract: Tarik data dari raw_earthquakes (PostgreSQL).
    2. Transform: Scaling data menggunakan standar yang sudah dilatih (is_training=False).
    3. Predict: Mengeksekusi model @champion (Hierarchical Clustering & Isolation Forest).
    4. Load: Mengirimkan hasil format JSON untuk dikonsumsi Frontend/Dashboard.
    """
    try:
        print("Menerima request untuk prediksi data gempa...")
        
        # 1. Extract
        df_raw = pipeline.load_from_db(db)
        if df_raw.empty:
            raise HTTPException(status_code=404, detail="Data gempa tidak ditemukan di database.")

        # 2. Transform
        df_processed = pipeline.prepare_features(df_raw, is_training=False)
        
        # 3. Inference (Memanggil AI)
        df_result = pipeline.predict_all(df_processed)
        
        # 4. Format Output JSON
        # Kita hanya memilih kolom esensial agar transfer data ke Frontend sangat ringan dan cepat
        cols_to_return = [
            'id', 'time', 'latitude', 'longitude', 'depth', 'magnitude', 
            'place', 'zona_klaster', 'is_anomaly'
        ]
        result_json = df_result[cols_to_return].to_dict(orient="records")
        
        return {
            "status": "success",
            "message": "Prediksi MLOps berhasil dieksekusi menggunakan model @champion.",
            "total_data": len(result_json),
            "data": result_json
        }
        
    except FileNotFoundError as e:
        # Menangkap error jika scaler belum di-training
        raise HTTPException(status_code=400, detail=f"Scaler Error: {str(e)}")
    except Exception as e:
        # Menangkap error general dari server atau MLflow
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    
