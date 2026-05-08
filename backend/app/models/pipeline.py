import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import text
from sklearn.preprocessing import StandardScaler
import joblib
import os
import mlflow.pyfunc
from dotenv import load_dotenv

# Memuat variabel environment dari file .env
load_dotenv()

class SeismoPipeline:
    def __init__(self):
        # 1. Batas Geografis Indonesia
        self.LAT_MIN, self.LAT_MAX = -11.0, 6.0
        self.LON_MIN, self.LON_MAX = 95.0, 141.0
        
        # 2. Setup Scaler
        self.scaler = StandardScaler()
        self.scaler_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../saved_models/scaler.joblib'))
        self.load_scaler() # Otomatis memuat scaler saat class dipanggil
        
        # 3. Setup MLflow Tracking & Models
        self.mlflow_uri = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
        mlflow.set_tracking_uri(self.mlflow_uri)
        
        self.cluster_model_name = os.getenv("MLFLOW_CLUSTERING_MODEL_NAME", "SeismoCluster_Clustering_Model")
        self.anomaly_model_name = os.getenv("MLFLOW_ANOMALY_MODEL_NAME", "SeismoCluster_Anomaly_Model")
        
        self.clustering_model = None
        self.anomaly_model = None

    # FASE 1: DATA ENGINEERING (EXTRACT)
    def load_from_db(self, db: Session) -> pd.DataFrame:
        """Mengekstrak data mentah dari PostgreSQL dan memfilter wilayah Indonesia."""
        query = text("""
            SELECT id, time, latitude, longitude, depth, magnitude, place 
            FROM raw_earthquakes 
            WHERE magnitude IS NOT NULL 
              AND latitude IS NOT NULL 
              AND longitude IS NOT NULL
        """)
        
        df = pd.read_sql(query, db.bind)
        
        df['time'] = pd.to_datetime(df['time'])
        df['year'] = df['time'].dt.year
        df['month'] = df['time'].dt.month
        df['day'] = df['time'].dt.day
        
        # Filter Spasial
        df_indo = df[
            (df['latitude'] >= self.LAT_MIN) & (df['latitude'] <= self.LAT_MAX) &
            (df['longitude'] >= self.LON_MIN) & (df['longitude'] <= self.LON_MAX)
        ].copy()
        
        return df_indo.reset_index(drop=True)

    # FASE 2: DATA TRANSFORMATION (SCALING)
    def prepare_features(self, df: pd.DataFrame, is_training: bool = False) -> pd.DataFrame:
        """
        Standarisasi nilai. 
        Jika is_training=True, scaler akan fit_transform (belajar pola baru).
        Jika is_training=False (Produksi), scaler HANYA transform (pakai pola lama).
        """
        cols_to_scale = ['latitude', 'longitude', 'depth', 'magnitude']
        
        if is_training:
            scaled_array = self.scaler.fit_transform(df[cols_to_scale])
            self.save_scaler()
        else:
            # Di tahap produksi/API, kita WAJIB menggunakan transform, bukan fit_transform
            if not os.path.exists(self.scaler_path):
                raise FileNotFoundError("Scaler belum dilatih! Jalankan training terlebih dahulu.")
            scaled_array = self.scaler.transform(df[cols_to_scale])
            
        df['latitude_scaled'] = scaled_array[:, 0]
        df['longitude_scaled'] = scaled_array[:, 1]
        df['depth_scaled'] = scaled_array[:, 2]
        df['magnitude_scaled'] = scaled_array[:, 3]
        
        return df

    def save_scaler(self):
        os.makedirs(os.path.dirname(self.scaler_path), exist_ok=True)
        joblib.dump(self.scaler, self.scaler_path)
        print(f"Scaler disimpan ke: {self.scaler_path}")
        
    def load_scaler(self):
        if os.path.exists(self.scaler_path):
            self.scaler = joblib.load(self.scaler_path)
        else:
            print("File scaler belum ada. Mode training diperlukan.")

    # FASE 3: MLOPS INFERENCE (PREDICTION)
    def load_mlflow_models(self):
        """Menarik model AI terbaru yang memiliki label @champion dari MLflow"""
        try:
            print("Mencari model AI @champion di MLflow...")
            self.clustering_model = mlflow.pyfunc.load_model(f"models:/{self.cluster_model_name}@champion")
            self.anomaly_model = mlflow.pyfunc.load_model(f"models:/{self.anomaly_model_name}@champion")
            print("Model Clustering & Anomaly berhasil dimuat!")
        except Exception as e:
            raise RuntimeError(f"Gagal memuat model dari MLflow. Pastikan server menyala. Error: {e}")

    def predict_all(self, df_processed: pd.DataFrame) -> pd.DataFrame:
        """
        Mengeksekusi model Hierarchical dan Isolation Forest ke data yang sudah di-scale.
        """
        if not self.clustering_model or not self.anomaly_model:
            self.load_mlflow_models()
            
        # Ekstrak fitur 4D
        X_infer = df_processed[['latitude_scaled', 'longitude_scaled', 'depth_scaled', 'magnitude_scaled']].values
        
        print("Mengeksekusi prediksi AI ganda...")
        # Prediksi 3 Zona Klaster (Hierarchical)
        clusters = self.clustering_model.predict(X_infer)
        
        # Prediksi Anomali Ekstrem (Isolation Forest)
        # Output asli: 1 (Normal), -1 (Anomali). Kita ubah ke Boolean agar mudah diolah frontend.
        anomalies_raw = self.anomaly_model.predict(X_infer)
        is_anomaly = [True if a == -1 else False for a in anomalies_raw]
        
        # Tempelkan hasil ke DataFrame
        df_processed['zona_klaster'] = clusters
        df_processed['is_anomaly'] = is_anomaly
        
        print(f"Prediksi selesai untuk {len(df_processed)} data gempa.")
        return df_processed