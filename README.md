# SeismoCluster

Dashboard real-time untuk pemantauan, analisis, dan pengelompokan gempa bumi wilayah Indonesia berbasis Machine Learning dan MLOps.

---

## Deskripsi Sistem

SeismoCluster mengambil data gempa bumi dari **USGS ComCat API**, memprosesnya melalui pipeline ETL, lalu menganalisisnya menggunakan 4 model Machine Learning yang dikelola via **MLflow Model Registry**. Hasil analisis ditampilkan secara visual pada dashboard interaktif berbasis peta dan grafik.

Sistem ini **bukan sistem prediksi gempa**, melainkan sistem **monitoring dan analisis pola gempa** yang sudah terjadi di wilayah Indonesia.

---

## Arsitektur Sistem

```
USGS ComCat API
      ↓
  ETL Pipeline
  (Extract → Transform → Load)
      ↓
PostgreSQL Database
(raw_earthquakes → processed_earthquakes)
      ↓
MLflow Model Registry (@champion)
      ↓
┌─────────────────────────────────────┐
│  KMeans        → Zona Wilayah       │
│  DBSCAN        → Hotspot Area       │
│  Isolation Forest → Anomali         │
│  Hierarchical  → Zona Hierarki      │
└─────────────────────────────────────┘
      ↓
FastAPI Backend (REST API)
      ↓
React Frontend (Dashboard)
```

---

## Teknologi yang Digunakan

### Backend

| Teknologi | Versi | Fungsi |
|---|---|---|
| Python | 3.x | Bahasa utama backend |
| FastAPI | - | REST API framework |
| Uvicorn | - | ASGI server |
| SQLAlchemy | - | ORM untuk PostgreSQL |
| psycopg2 | - | PostgreSQL driver |
| MLflow | 3.x | Model registry & experiment tracking |
| scikit-learn | - | Library ML (KMeans, DBSCAN, dll) |
| pandas | - | Manipulasi data |
| numpy | - | Komputasi numerik |
| joblib | - | Persistensi scaler |
| APScheduler | - | Scheduler ETL otomatis tiap 6 jam |
| requests | - | Konsumsi USGS API |
| python-dotenv | - | Manajemen environment variable |

### Frontend

| Teknologi | Versi | Fungsi |
|---|---|---|
| React | 19 | UI framework |
| Vite | - | Build tool & dev server |
| React Router DOM | 7 | Client-side routing |
| Axios | - | HTTP client ke backend |
| Leaflet + React-Leaflet | - | Peta interaktif |
| Chart.js + React-Chartjs-2 | - | Visualisasi grafik |
| Recharts | - | Grafik tambahan |
| Lucide React | - | Icon library |
| SASS | - | CSS preprocessor |

### Infrastruktur

| Teknologi | Fungsi |
|---|---|
| PostgreSQL | Database utama |
| MLflow Server | Model registry & tracking UI |
| SQLite (`mlflow.db`) | Backend store MLflow |

---

## Model Machine Learning

### 1. KMeans Clustering
- **Input:** Koordinat geografis (latitude & longitude dalam radian)
- **Output:** `zona_klaster` (0, 1, 2, ...)
- **Fungsi:** Membagi wilayah Indonesia menjadi zona-zona gempa dari barat ke timur
- **Model Name:** `SeismoCluster_Clustering_Model_KMeans`

### 2. DBSCAN (Hotspot Detection)
- **Input:** Koordinat geografis (latitude & longitude dalam radian)
- **Output:** `hotspot_zone` (-1 = noise/terisolasi, 0+ = hotspot)
- **Fungsi:** Mendeteksi area konsentrasi gempa tinggi (hotspot)
- **Model Name:** `SeismoCluster_Hotspot_Model`

### 3. Isolation Forest (Anomaly Detection)
- **Input:** latitude, longitude, depth, magnitude (sudah di-scale)
- **Output:** `is_anomaly` (True / False)
- **Fungsi:** Mendeteksi gempa yang tidak wajar secara statistik (terlalu dalam, terlalu kuat, atau kombinasi keduanya)
- **Model Name:** `SeismoCluster_Anomaly_Model_ISF`

### 4. Hierarchical Clustering (Ward Linkage)
- **Input:** Koordinat geografis (latitude & longitude dalam radian)
- **Output:** `hierarchy_label`
- **Fungsi:** Pengelompokan hierarki sebagai alternatif KMeans
- **Model Name:** `SeismoCluster_Hierarchy_Model`

> Semua model dikelola di MLflow Model Registry dan diload menggunakan alias `@champion`.

---

## Struktur Project

```
seismocluster/
├── backend/
│   ├── api/
│   │   ├── main.py                  # Entry point FastAPI
│   │   └── routes/
│   │       ├── ml.py                # Endpoint ML (/api/v1/ml)
│   │       ├── cluster.py           # Endpoint clustering (/api/v1/clusters)
│   │       ├── earthquake.py        # Endpoint CRUD gempa (/api/v1/earthquakes)
│   │       └── summary.py           # Endpoint statistik (/api/v1/summary)
│   ├── app/
│   │   ├── config/
│   │   │   └── database.py          # Koneksi PostgreSQL
│   │   ├── etl/
│   │   │   ├── extract.py           # Ambil data dari USGS API
│   │   │   ├── transform.py         # Transformasi data
│   │   │   ├── load.py              # Simpan ke database
│   │   │   └── pipeline.py          # Orkestrasi ETL
│   │   ├── models/
│   │   │   ├── pipeline.py          # SeismoPipeline (load model, predict)
│   │   │   ├── clustering/          # KMeans, DBSCAN, Hierarchical
│   │   │   └── anomaly/             # Isolation Forest
│   │   ├── services/
│   │   │   ├── cluster_service.py   # Orkestrasi training pipeline
│   │   │   ├── ml_service.py        # Jalankan clustering dari processed data
│   │   │   └── summary_service.py   # Statistik ringkasan
│   │   ├── repositories/
│   │   │   └── earthquake_repository.py  # Query database
│   │   └── saved_models/
│   │       └── scaler.joblib        # StandardScaler tersimpan
│   ├── .env                         # Konfigurasi environment
│   ├── mlflow.db                    # SQLite store MLflow
│   └── check_models.py              # Script cek status model MLflow
└── frontend/
    └── src/
        ├── pages/
        │   ├── Landing.jsx          # Halaman utama
        │   ├── ClusterMap.jsx       # Peta zona clustering
        │   ├── Anomaly.jsx          # Dashboard anomali
        │   ├── Hotspot.jsx          # Peta hotspot DBSCAN
        │   ├── Hierarchy.jsx        # Visualisasi hierarchical
        │   ├── Realtime.jsx         # Prediksi real-time
        │   ├── Trend.jsx            # Tren gempa
        │   ├── Movement.jsx         # Pergerakan gempa
        │   └── Centroid.jsx         # Centroid cluster
        └── components/              # Komponen reusable
```

---

## API Endpoints

### Machine Learning
| Method | Endpoint | Deskripsi |
|---|---|---|
| GET | `/api/v1/ml/predict-earthquakes` | Prediksi real-time menggunakan model @champion |
| GET | `/api/v1/ml/models` | Cek status model di MLflow Registry |

### Clustering
| Method | Endpoint | Deskripsi |
|---|---|---|
| POST | `/api/v1/clusters/etl` | Ambil data terbaru dari USGS |
| POST | `/api/v1/clusters/train` | Jalankan full ML pipeline |
| GET | `/api/v1/clusters/results` | Hasil clustering dari database |
| GET | `/api/v1/clusters/anomalies` | Daftar gempa anomali |
| GET | `/api/v1/clusters/hierarchy/summary` | Statistik zona hierarki |

### Data Gempa
| Method | Endpoint | Deskripsi |
|---|---|---|
| GET | `/api/v1/earthquakes/` | Semua data gempa (dengan pagination) |
| GET | `/api/v1/earthquakes/{id}` | Detail gempa by ID |
| POST | `/api/v1/earthquakes/` | Tambah data gempa manual |
| PUT | `/api/v1/earthquakes/{id}` | Update data gempa |
| DELETE | `/api/v1/earthquakes/{id}` | Hapus data gempa |

### Statistik
| Method | Endpoint | Deskripsi |
|---|---|---|
| GET | `/api/v1/summary/` | Ringkasan data gempa |
| GET | `/api/v1/summary/stats` | Statistik keseluruhan |
| GET | `/api/v1/scheduler/status` | Status ETL scheduler |

---

## Cara Menjalankan

### Prasyarat
- Python 3.x + virtual environment
- Node.js
- PostgreSQL (berjalan di port 5432)

### 1. Jalankan MLflow Server
```powershell
cd C:\seismocluster\backend
mlflow server --backend-store-uri sqlite:///mlflow.db --host 0.0.0.0 --port 5000
```

### 2. Jalankan Backend
```powershell
cd C:\seismocluster\backend
uvicorn api.main:app --reload --host 127.0.0.1 --port 8000
```

### 3. Jalankan Frontend
```powershell
cd C:\seismocluster\frontend
npm run dev
```

> **Urutan penting:** MLflow harus jalan sebelum backend agar model dapat di-load saat endpoint ML dipanggil.

### 4. Konfigurasi `.env`
```env
DB_NAME=SeismoCluster
DB_USER=postgres
DB_PASS=your_password
DB_HOST=localhost
DB_PORT=5432

MLFLOW_TRACKING_URI=http://localhost:5000

MLFLOW_CLUSTERING_MODEL_NAME=SeismoCluster_Clustering_Model_KMeans
MLFLOW_HOTSPOT_MODEL_NAME=SeismoCluster_Hotspot_Model
MLFLOW_ANOMALY_MODEL_NAME=SeismoCluster_Anomaly_Model_ISF
MLFLOW_HIERARCHY_MODEL_NAME=SeismoCluster_Hierarchy_Model
```

### 5. Cek Status Model MLflow
```powershell
cd C:\seismocluster\backend
python check_models.py
```

---

## Data Sumber

- **API:** [USGS Earthquake Hazards Program - ComCat API](https://earthquake.usgs.gov/fdsnws/event/1/)
- **Wilayah:** Indonesia (Latitude: -11.0 s/d 6.0, Longitude: 95.0 s/d 141.0)
- **Periode:** 2010 s/d sekarang
- **Update:** Otomatis setiap 6 jam via APScheduler (incremental)

---

## ETL Scheduler

Backend menjalankan ETL otomatis setiap **6 jam** menggunakan APScheduler. ETL berjalan secara incremental — hanya mengambil data gempa terbaru sejak update terakhir, bukan mengulang dari awal.

Cek jadwal ETL berikutnya:
```
GET /api/v1/scheduler/status
```
