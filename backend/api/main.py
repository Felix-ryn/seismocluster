from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import earthquake, cluster, summary

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(earthquake.router, prefix="/earthquakes")
app.include_router(cluster.router, prefix="/clusters")
app.include_router(summary.router, prefix="/summary")

@app.get("/")
def root():
    return {"message": "API running"}