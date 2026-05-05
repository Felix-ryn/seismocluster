from fastapi import FastAPI
from api.routes import ml # Mengimpor file router yang baru dibuat

app = FastAPI(
    title="SeismoCluster API",
    description="Backend Service untuk Dashboard Real-Time Pemantauan Gempa",
    version="1.0.0"
)

# Mendaftarkan router ML ke dalam aplikasi utama
app.include_router(ml.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to SeismoCluster API"}