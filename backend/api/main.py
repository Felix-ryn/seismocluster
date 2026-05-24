from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from api.routes import ml, earthquake, cluster, summary
from app.config.database import get_connection
from app.etl.pipeline import run_pipeline as run_etl



ETL_INTERVAL_HOURS = 6   # jalan ETL setiap 6 jam


def run_migrations():
    """Pastikan kolom-kolom baru ada sebelum server melayani request."""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "ALTER TABLE earthquake_clusters "
            "ADD COLUMN IF NOT EXISTS hierarchy_label INTEGER;"
        )
        conn.commit()
        cur.close()
        conn.close()
        print("Migration OK: hierarchy_label column ensured.")
    except Exception as e:
        print(f"Migration warning: {e}")


def scheduled_etl():
    """Job yang dijalankan otomatis oleh scheduler."""
    print(f"[Scheduler] ETL otomatis dimulai...")
    try:
        inserted = run_etl()
        print(f"[Scheduler] ETL selesai — {inserted} data baru.")
    except Exception as e:
        print(f"[Scheduler] ETL gagal: {e}")


scheduler = BackgroundScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    run_migrations()

    # Jalankan ETL otomatis setiap ETL_INTERVAL_HOURS jam
    scheduler.add_job(
        scheduled_etl,
        trigger=IntervalTrigger(hours=ETL_INTERVAL_HOURS),
        id="auto_etl",
        name="ETL Otomatis USGS",
        replace_existing=True,
    )
    scheduler.start()
    print(f"[Scheduler] ETL otomatis aktif — interval {ETL_INTERVAL_HOURS} jam.")

    yield

    scheduler.shutdown()
    print("[Scheduler] Scheduler dihentikan.")


app = FastAPI(
    title="SeismoCluster API",
    description="Backend Service MLOps untuk Dashboard Real-Time Pemantauan Gempa",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ml.router)
app.include_router(earthquake.router)
app.include_router(cluster.router)
app.include_router(summary.router)


@app.get("/")
def read_root():
    return {
        "status": "online",
        "message": "Welcome to SeismoCluster API Production Server",
        "ml_engine": "Active",
        "etl_scheduler": f"Aktif — setiap {ETL_INTERVAL_HOURS} jam",
    }


@app.get("/api/v1/scheduler/status")
def scheduler_status():
    """Cek status dan jadwal ETL berikutnya."""
    jobs = []
    for job in scheduler.get_jobs():
        jobs.append({
            "id": job.id,
            "name": job.name,
            "next_run": str(job.next_run_time),
        })
    return {
        "scheduler_running": scheduler.running,
        "jobs": jobs,
    }
