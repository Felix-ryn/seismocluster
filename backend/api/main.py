from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import ml # Mengimpor file router yang baru dibuat

app = FastAPI(
    title="SeismoCluster API",
    description="Backend Service MLOps untuk Dashboard Real-Time Pemantauan Gempa",
    version="1.0.0"
)

# KONFIGURASI CORS (SANGAT KRUSIAL UNTUK INTEGRASI FRONTEND)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Saat produksi/deploy, ganti "*" dengan URL domain Frontend Anda
    allow_credentials=True,
    allow_methods=["*"],  # Mengizinkan GET, POST, PUT, DELETE, dll.
    allow_headers=["*"],
)

# Mendaftarkan router ML ke dalam aplikasi utama
# Karena di ml.py sudah ada prefix="/api/v1/ml", kita cukup include_router saja
app.include_router(ml.router)

@app.get("/")
def read_root():
    return {
        "status": "online",
        "message": "Welcome to SeismoCluster API Production Server",
        "ml_engine": "Active"
    }