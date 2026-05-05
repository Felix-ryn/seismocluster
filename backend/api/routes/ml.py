from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.services.cluster_service import ClusterService

# Membuat router khusus untuk operasi Machine Learning
router = APIRouter(prefix="/api/v1/ml", tags=["Machine Learning Operations"])

@router.post("/run-pipeline")
def trigger_ml_pipeline(db: Session = Depends(get_db)):
    """
    Endpoint ini akan mengeksekusi seluruh proses MLOps:
    1. Extract data dari raw_earthquakes
    2. Transform (Scaling & Cleaning)
    3. Eksekusi K-Means & DBSCAN
    4. Evaluasi Model
    5. Load hasil ke PostgreSQL
    """
    try:
        # Inisialisasi Service dan Eksekusi
        service = ClusterService(db_session=db)
        result = service.execute_ml_pipeline()
        
        if result.get("status") == "error":
            raise HTTPException(status_code=400, detail=result.get("message"))
            
        return result
        
    except Exception as e:
        # Menangkap error jika terjadi kegagalan di level database atau modeling
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")