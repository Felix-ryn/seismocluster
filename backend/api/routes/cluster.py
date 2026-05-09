from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

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

    service = ClusterService(db)

    result = service.execute_ml_pipeline()

    return {
        "status": "success",
        "result": result
    }