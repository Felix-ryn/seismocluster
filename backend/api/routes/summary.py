from fastapi import APIRouter, HTTPException
import traceback

from app.services.summary_service import get_summary, get_summary_stats

router = APIRouter(
    prefix="/api/v1/summary",
    tags=["Summary"]
)


@router.get("/")
def summary():
    """Ringkasan per cluster: jumlah gempa, rata-rata magnitudo, dan rata-rata kedalaman."""
    try:
        data = get_summary()
        if not data:
            return {
                "status": "success",
                "message": "Belum ada data clustering. Jalankan POST /api/v1/clusters/train.",
                "data": []
            }
        return {
            "status": "success",
            "data": data
        }
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
def summary_stats():
    """Statistik keseluruhan: total cluster, total gempa diproses, total anomali, total noise."""
    try:
        stats = get_summary_stats()
        return {
            "status": "success",
            "data": stats
        }
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
