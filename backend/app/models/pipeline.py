import pandas as pd
import numpy as np

from sqlalchemy.orm import Session
from sqlalchemy import text

from sklearn.preprocessing import StandardScaler

import joblib
import os

import mlflow
import mlflow.sklearn

from dotenv import load_dotenv

# ==========================================
# LOAD ENV
# ==========================================
load_dotenv()


class SeismoPipeline:

    def __init__(self):

        # ==========================================
        # BATAS INDONESIA
        # ==========================================
        self.LAT_MIN = -11.0
        self.LAT_MAX = 6.0

        self.LON_MIN = 95.0
        self.LON_MAX = 141.0

        # ==========================================
        # SCALER
        # ==========================================
        self.scaler = StandardScaler()

        self.scaler_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "../saved_models/scaler.joblib"
            )
        )

        self.load_scaler()

        # ==========================================
        # MLFLOW
        # ==========================================
        self.mlflow_uri = os.getenv(
            "MLFLOW_TRACKING_URI",
            "http://localhost:5000"
        )

        mlflow.set_tracking_uri(
            self.mlflow_uri
        )

        # ==========================================
        # MODEL NAMES
        # ==========================================
        self.cluster_model_name = os.getenv(
            "MLFLOW_CLUSTERING_MODEL_NAME",
            "SeismoCluster_Hierarchy_Model"
        )

        self.anomaly_model_name = os.getenv(
            "MLFLOW_ANOMALY_MODEL_NAME",
            "SeismoCluster_Anomaly_Model_ISF"
        )

        # ==========================================
        # MODEL OBJECT
        # ==========================================
        self.clustering_model = None
        self.anomaly_model = None

    # ==========================================
    # LOAD DATA
    # ==========================================
    def load_from_db(
        self,
        db: Session
    ) -> pd.DataFrame:

        query = text("""
            SELECT
                id,
                time,
                latitude,
                longitude,
                depth,
                magnitude,
                place
            FROM raw_earthquakes
            WHERE magnitude IS NOT NULL
              AND latitude IS NOT NULL
              AND longitude IS NOT NULL
            ORDER BY time DESC
            LIMIT 1000
        """)

        df = pd.read_sql(
            query,
            db.bind
        )

        # ==========================================
        # DATETIME
        # ==========================================
        df['time'] = pd.to_datetime(
            df['time']
        )

        # ==========================================
        # FILTER INDONESIA
        # ==========================================
        df = df[
            (df['latitude'] >= self.LAT_MIN) &
            (df['latitude'] <= self.LAT_MAX) &
            (df['longitude'] >= self.LON_MIN) &
            (df['longitude'] <= self.LON_MAX)
        ].copy()

        return df.reset_index(drop=True)

    # ==========================================
    # FEATURE ENGINEERING
    # ==========================================
    def prepare_features(
        self,
        df: pd.DataFrame,
        is_training: bool = False
    ) -> pd.DataFrame:

        cols_to_scale = [
            'latitude',
            'longitude',
            'depth',
            'magnitude'
        ]

        # ==========================================
        # TRAINING
        # ==========================================
        if is_training:

            scaled_array = self.scaler.fit_transform(
                df[cols_to_scale]
            )

            self.save_scaler()

        # ==========================================
        # INFERENCE
        # ==========================================
        else:

            if not os.path.exists(
                self.scaler_path
            ):
                raise FileNotFoundError(
                    "Scaler belum tersedia."
                )

            scaled_array = self.scaler.transform(
                df[cols_to_scale]
            )

        # ==========================================
        # SAVE FEATURES
        # ==========================================
        df['latitude_scaled'] = scaled_array[:, 0]
        df['longitude_scaled'] = scaled_array[:, 1]
        df['depth_scaled'] = scaled_array[:, 2]
        df['magnitude_scaled'] = scaled_array[:, 3]

        return df

    # ==========================================
    # SAVE SCALER
    # ==========================================
    def save_scaler(self):

        os.makedirs(
            os.path.dirname(
                self.scaler_path
            ),
            exist_ok=True
        )

        joblib.dump(
            self.scaler,
            self.scaler_path
        )

        print(
            f"Scaler berhasil disimpan: {self.scaler_path}"
        )

    # ==========================================
    # LOAD SCALER
    # ==========================================
    def load_scaler(self):

        if os.path.exists(
            self.scaler_path
        ):

            self.scaler = joblib.load(
                self.scaler_path
            )

            print(
                "Scaler berhasil dimuat"
            )

        else:

            print(
                "Scaler belum tersedia"
            )

    # ==========================================
    # LOAD MODEL MLFLOW
    # ==========================================
    def load_mlflow_models(self):

        try:

            print("=" * 50)
            print("Menghubungkan ke MLflow")

            print(
                f"Load Clustering Model: {self.cluster_model_name}"
            )

            self.clustering_model = mlflow.sklearn.load_model(
                f"models:/{self.cluster_model_name}@champion"
            )

            print(
                f"Load Anomaly Model: {self.anomaly_model_name}"
            )

            self.anomaly_model = mlflow.sklearn.load_model(
                f"models:/{self.anomaly_model_name}@champion"
            )

            print(
                "Semua model berhasil dimuat"
            )

            print("=" * 50)

        except Exception as e:

            raise RuntimeError(
                f"Gagal load model MLflow: {str(e)}"
            )

    # ==========================================
    # PREDICT ALL
    # ==========================================
    def predict_all(
        self,
        df_processed: pd.DataFrame
    ) -> pd.DataFrame:

        # ==========================================
        # LOAD MODEL
        # ==========================================
        if (
            self.clustering_model is None or
            self.anomaly_model is None
        ):
            self.load_mlflow_models()

        # ==========================================
        # DATA SPATIAL
        # SESUAI NOTEBOOK
        # ==========================================
        df_processed['lat_radian'] = np.radians(
            df_processed['latitude']
        )

        df_processed['lon_radian'] = np.radians(
            df_processed['longitude']
        )

        coords_radians = df_processed[
            [
                'lat_radian',
                'lon_radian'
            ]
        ]

        # ==========================================
        # DATA 4D ANOMALY
        # ==========================================
        X_anomaly = df_processed[
            [
                'latitude_scaled',
                'longitude_scaled',
                'depth_scaled',
                'magnitude_scaled'
            ]
        ]

        # ==========================================
        # HIERARCHICAL CLUSTERING
        # ==========================================
        print(
            "Menjalankan hierarchical clustering..."
        )

        clusters = self.clustering_model.fit_predict(
            coords_radians
        )

        # ==========================================
        # ISOLATION FOREST
        # ==========================================
        print(
            "Menjalankan anomaly detection..."
        )

        anomalies = self.anomaly_model.predict(
            X_anomaly
        )

        # ==========================================
        # BOOLEAN ANOMALY
        # ==========================================
        is_anomaly = [
            True if x == -1 else False
            for x in anomalies
        ]

        # ==========================================
        # SAVE RESULT
        # ==========================================
        df_processed['zona_klaster'] = clusters

        df_processed['is_anomaly'] = is_anomaly

        print(
            f"Prediksi selesai untuk {len(df_processed)} data"
        )

        return df_processed