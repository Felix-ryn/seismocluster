from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import traceback

from app.config.database import get_db
from app.services.cluster_service import ClusterService

router = APIRouter(
    prefix="/api/v1/clusters",
    tags=["Clusters"]
)


@router.post("/train")
def train_cluster(
    db: Session = Depends(get_db)
):

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

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )