from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import traceback

from app.config.database import get_db
from app.services.cluster_service import ClusterService
from app.repositories.earthquake_repository import (
    get_cluster_results,
    get_cluster_result_count,
    get_anomaly_earthquakes,
    get_hierarchy_summary,
)

router = APIRouter(
    prefix="/api/v1/clusters",
    tags=["Clusters"]
)


@router.post("/etl")
def run_etl(db: Session = Depends(get_db)):
    """Ambil data gempa terbaru dari USGS dan simpan ke database."""
    try:
        print("=" * 50)
        print("START ETL PIPELINE")

        service = ClusterService(db)
        result = service.run_etl_pipeline()

        print("ETL SELESAI")
        print("=" * 50)

        return {
            "status": "success",
            "result": result
        }

    except Exception as e:
        print("ERROR ETL")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/train")
def train_cluster(db: Session = Depends(get_db)):
    """Jalankan full ML pipeline: clustering + anomaly detection + simpan ke DB."""
    try:
        print("=" * 50)
        print("START TRAINING PIPELINE")

        service = ClusterService(db)
        result = service.execute_ml_pipeline()

        print("TRAINING BERHASIL")
        print("=" * 50)

        return {
            "status": "success",
            "result": result
        }

    except Exception as e:
        print("=" * 50)
        print("ERROR TRAINING")
        print(str(e))
        traceback.print_exc()
        print("=" * 50)

        raise HTTPException(status_code=500, detail=str(e))


@router.get("/results")
def get_results(
    imit: int = Query(default=32000, ge=1, le=35000, description="Jumlah data yang diambil"),
    offset: int = Query(default=0, ge=0, description="Offset untuk pagination")
):
    """Ambil hasil clustering dari database (earthquake_clusters join raw_earthquakes)."""
    try:
        data = get_cluster_results(limit=limit, offset=offset)
        total = get_cluster_result_count()

        if not data:
            return {
                "status": "success",
                "message": "Belum ada hasil clustering. Jalankan POST /train terlebih dahulu.",
                "total": 0,
                "data": []
            }

        return {
            "status": "success",
            "total": total,
            "limit": limit,
            "offset": offset,
            "data": data
        }

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/hierarchy/summary")
def get_hierarchy_summary_endpoint():
    """Statistik per zona hierarchical clustering (Ward linkage)."""
    try:
        data = get_hierarchy_summary()
        return {
            "status": "success",
            "total_zones": len(data),
            "data": data
        }
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/anomalies")
def get_anomalies(
    limit: int = Query(default=500, ge=1, le=2000, description="Jumlah anomali yang diambil")
):
    """Ambil gempa yang terdeteksi sebagai anomali (kedalaman/magnitudo ekstrem)."""
    try:
        data = get_anomaly_earthquakes(limit=limit)

        return {
            "status": "success",
            "total_anomalies": len(data),
            "data": data
        }

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
