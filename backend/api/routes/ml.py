from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import traceback

# Import dependensi
from app.config.database import get_db
from app.models.pipeline import SeismoPipeline

# Membuat router khusus untuk operasi Machine Learning
router = APIRouter(
    prefix="/api/v1/ml",
    tags=["Machine Learning Operations"]
)

# Inisialisasi pipeline global
pipeline = SeismoPipeline()


@router.get("/predict-earthquakes")
def predict_earthquakes_endpoint(
    db: Session = Depends(get_db)
):
    """
    Endpoint Produksi untuk Inferensi MLOps:
    1. Extract: Tarik data dari PostgreSQL
    2. Transform: Scaling data
    3. Predict: Prediksi clustering & anomaly
    4. Return JSON
    """

    try:

        print("=" * 50)
        print("Menerima request untuk prediksi data gempa...")

        # ==========================================
        # 1. LOAD DATA
        # ==========================================
        print("STEP 1 - Load data dari database")

        df_raw = pipeline.load_from_db(db)

        if df_raw.empty:
            raise HTTPException(
                status_code=404,
                detail="Data gempa tidak ditemukan di database."
            )

        print(f"Jumlah data berhasil diambil: {len(df_raw)}")


        # ==========================================
        # 2. PREPROCESSING
        # ==========================================
        print("STEP 2 - Scaling & feature engineering")

        df_processed = pipeline.prepare_features(
            df_raw,
            is_training=False
        )

        print("Preprocessing berhasil")


        # ==========================================
        # 3. PREDICTION
        # ==========================================
        print("STEP 3 - Menjalankan model MLflow")

        df_result = pipeline.predict_all(df_processed)

        print("Prediksi berhasil")


        # ==========================================
        # 4. FORMAT RESPONSE
        # ==========================================
        cols_to_return = [
            'id',
            'time',
            'latitude',
            'longitude',
            'depth',
            'magnitude',
            'place',
            'zona_klaster',
            'is_anomaly'
        ]

        result_json = df_result[
            cols_to_return
        ].to_dict(orient="records")

        print("Response berhasil dibuat")
        print("=" * 50)

        return {
            "status": "success",
            "message": "Prediksi MLOps berhasil dijalankan",
            "total_data": len(result_json),
            "data": result_json
        }

    except FileNotFoundError as e:

        print("ERROR SCALER:")
        print(str(e))

        raise HTTPException(
            status_code=400,
            detail=f"Scaler Error: {str(e)}"
        )

    except Exception as e:

        print("=" * 50)
        print("ERROR ML PIPELINE")
        print(str(e))

        traceback.print_exc()

        print("=" * 50)

        raise HTTPException(
            status_code=500,
            detail=f"Internal Server Error: {str(e)}"
        )