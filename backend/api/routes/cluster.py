from fastapi import APIRouter
from app.services.cluster_service import get_clusters
from app.services.ml_service import run_clustering

router = APIRouter()

@router.get("/")
def clusters():
    return get_clusters()

@router.post("/run")
def run():
    return run_clustering()