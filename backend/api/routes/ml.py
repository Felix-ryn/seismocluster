from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import traceback

from app.config.database import get_db
from app.models.pipeline import SeismoPipeline

router = APIRouter(
    prefix="/api/v1/ml",
    tags=["Machine Learning Operations"]
)

# GLOBAL PIPELINE
pipeline = SeismoPipeline()


@router.get("/predict-earthquakes")
def predict_earthquakes_endpoint(
    limit: int = 100,
    db: Session = Depends(get_db)
):

    try:

        print("=" * 50)
        print("Menerima request prediksi gempa")

        # ==========================================
        # LOAD DATA
        # ==========================================
        print("STEP 1 - Load data")

        df_raw = pipeline.load_from_db(db)

        if df_raw.empty:

            raise HTTPException(
                status_code=404,
                detail="Data gempa kosong"
            )

        print(
            f"Jumlah data berhasil diambil: {len(df_raw)}"
        )

        # ==========================================
        # PREPROCESSING
        # ==========================================
        print("STEP 2 - Preprocessing")

        df_processed = pipeline.prepare_features(
            df_raw,
            is_training=False
        )

        print("Preprocessing berhasil")

        # ==========================================
        # PREDICTION
        # ==========================================
        print("STEP 3 - Prediction")

        df_result = pipeline.predict_all(
            df_processed
        )

        print("Prediksi berhasil")

        # ==========================================
        # LIMIT RESPONSE
        # ==========================================
        df_result = df_result.head(limit)

        # ==========================================
        # RESPONSE
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
            "message": "Prediksi berhasil",
            "total_data": len(result_json),
            "data": result_json
        }

    except FileNotFoundError as e:

        print("ERROR SCALER")
        print(str(e))

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:

        print("=" * 50)
        print("ERROR ML PIPELINE")
        print(str(e))

        traceback.print_exc()

        print("=" * 50)

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )