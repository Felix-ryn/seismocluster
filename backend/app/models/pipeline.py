# filepath: backend/app/models/clustering/pipeline.py
import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import text
from sklearn.preprocessing import StandardScaler
import joblib
import os


class SeismoDataPipeline:
    def __init__(self):
        # Batas Geografis Indonesia
        self.LAT_MIN, self.LAT_MAX = -11.0, 6.0
        self.LON_MIN, self.LON_MAX = 95.0, 141.0
        self.scaler = StandardScaler()
        self.scaler_path = os.path.join(os.path.dirname(__file__), '../saved_models/scaler.joblib')

    def load_from_db(self, db: Session) -> pd.DataFrame:
        """
        Extract & Transform Tahap 1:
        Mengekstrak data mentah, membersihkan null, dan filtering spasial & temporal.
        """
        query = text("""
            SELECT id, time, latitude, longitude, depth, magnitude, place 
            FROM raw_earthquakes 
            WHERE magnitude IS NOT NULL 
              AND latitude IS NOT NULL 
              AND longitude IS NOT NULL
        """)
        
        # Eksekusi query
        df = pd.read_sql(query, db.bind)
        
        # Parsing Waktu untuk mengisi kolom year, month, day di processed_earthquakes
        df['time'] = pd.to_datetime(df['time'])
        df['year'] = df['time'].dt.year
        df['month'] = df['time'].dt.month
        df['day'] = df['time'].dt.day
        
        # Filter Spasial: Hanya ambil titik gempa wilayah Indonesia
        df_indo = df[
            (df['latitude'] >= self.LAT_MIN) & (df['latitude'] <= self.LAT_MAX) &
            (df['longitude'] >= self.LON_MIN) & (df['longitude'] <= self.LON_MAX)
        ].copy()
        
        return df_indo.reset_index(drop=True)
    

    def prepare_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transform Tahap 2:
        Standarisasi nilai (scaling) untuk Machine Learning dan Database.
        """
        cols_to_scale = ['latitude', 'longitude', 'depth', 'magnitude']
        
        # Melakukan proses scaling
        scaled_array = self.scaler.fit_transform(df[cols_to_scale])
        
        # Menyimpan hasil scaling ke kolom baru sesuai dengan kolom di processed_earthquakes
        df['latitude_scaled'] = scaled_array[:, 0]
        df['longitude_scaled'] = scaled_array[:, 1]
        df['depth_scaled'] = scaled_array[:, 2]
        df['magnitude_scaled'] = scaled_array[:, 3]
        
        # Mengembalikan DataFrame yang sudah komplit dengan fitur asli dan scaled
        return df
    
    def save_scaler(self):
        """meyimpan objek scaler ke file """
        os.makedirs(os.path.dirname(self.scaler_path), exist_ok=True)
        joblib.dump(self.scaler, self.scaler_path)
        print("Scaler berhasil disimpan ke:", self.scaler_path)
        
    def load_scaler(self):
        """memuat objek scaler dari file jika ada"""
        if os.path.exists(self.scaler_path):
            self.scaler = joblib.load(self.scaler_path)
            print("Scaler berhasil dimuat dari:", self.scaler_path)
        else:
            print("File scaler tidak ditemukan. Pastikan untuk menjalankan save_scaler() setelah fit_transform.")