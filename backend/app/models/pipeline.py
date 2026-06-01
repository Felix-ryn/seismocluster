import pandas as pd
import numpy as np

from sqlalchemy.orm import Session
from sqlalchemy import text

from sklearn.preprocessing import StandardScaler

import joblib
import os

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
        # SAVED MODELS DIR
        # ==========================================
        self.models_dir = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "../saved_models"
            )
        )

        # ==========================================
        # SCALER
        # ==========================================
        self.scaler = StandardScaler()

        self.scaler_path = os.path.join(
            self.models_dir,
            "scaler.joblib"
        )

        self.load_scaler()

        # ==========================================
        # MODEL OBJECT
        # ==========================================
        self.clustering_model = None
        self.hotspot_model    = None
        self.anomaly_model    = None
        self.hierarchy_model  = None

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
              AND latitude  BETWEEN :lat_min  AND :lat_max
              AND longitude BETWEEN :lon_min  AND :lon_max
            ORDER BY time DESC
        """)

        df = pd.read_sql(
            query,
            db.connection(),
            params={
                "lat_min": self.LAT_MIN,
                "lat_max": self.LAT_MAX,
                "lon_min": self.LON_MIN,
                "lon_max": self.LON_MAX,
            }
        )

        df['time'] = pd.to_datetime(df['time'])

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

        df['year'] = df['time'].dt.year
        df['month'] = df['time'].dt.month
        df['day'] = df['time'].dt.day

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
    # LOAD MODEL DARI JOBLIB LOKAL
    # ==========================================
    def load_mlflow_models(self):

        try:

            print("=" * 50)
            print("Load model dari local joblib...")

            self.clustering_model = joblib.load(
                os.path.join(self.models_dir, "clustering_model.joblib")
            )
            print("Load Clustering Model: OK")

            self.hotspot_model = joblib.load(
                os.path.join(self.models_dir, "hotspot_model.joblib")
            )
            print("Load Hotspot Model: OK")

            self.anomaly_model = joblib.load(
                os.path.join(self.models_dir, "anomaly_model.joblib")
            )
            print("Load Anomaly Model: OK")

            self.hierarchy_model = joblib.load(
                os.path.join(self.models_dir, "hierarchy_model.joblib")
            )
            print("Load Hierarchy Model: OK")

            print("Semua model berhasil dimuat")
            print("=" * 50)

        except Exception as e:

            raise RuntimeError(
                f"Gagal load model dari joblib: {str(e)}"
            )

    # ==========================================
    # PREDICT ALL
    # ==========================================
    def predict_all(
        self,
        df_processed: pd.DataFrame
    ) -> pd.DataFrame:

        if (
            self.clustering_model is None or
            self.hotspot_model    is None or
            self.anomaly_model    is None or
            self.hierarchy_model  is None
        ):
            self.load_mlflow_models()

        df_processed['lat_radian'] = np.radians(
            df_processed['latitude']
        )

        df_processed['lon_radian'] = np.radians(
            df_processed['longitude']
        )

        coords_radians = df_processed[
            ['lat_radian', 'lon_radian']
        ].values

        X_anomaly = df_processed[
            [
                'latitude_scaled',
                'longitude_scaled',
                'depth_scaled',
                'magnitude_scaled'
            ]
        ].values

        print("Menjalankan KMeans clustering...")

        clusters = self.clustering_model.predict(
            coords_radians
        )

        unique_labels = np.unique(clusters)
        mean_lons = {
            lbl: df_processed['longitude'].values[clusters == lbl].mean()
            for lbl in unique_labels
        }
        sorted_labels = sorted(unique_labels, key=lambda l: mean_lons[l])
        label_map = {old: new for new, old in enumerate(sorted_labels)}
        clusters = np.array([label_map[c] for c in clusters], dtype=np.int32)
        print(
            f"Relabeling cluster selesai: "
            + ", ".join(
                f"{old}→{label_map[old]} (lon≈{mean_lons[old]:.1f}°)"
                for old in sorted_labels
            )
        )

        print("Menjalankan hotspot detection...")

        hotspot_zones = self.hotspot_model.fit_predict(
            coords_radians
        )

        print("Menjalankan anomaly detection...")

        anomalies = self.anomaly_model.predict(
            X_anomaly
        )

        print("Menjalankan hierarchical clustering...")

        N = len(coords_radians)
        HIER_MAX = 1500

        if N > HIER_MAX:
            print(
                f"Subsample {HIER_MAX} dari {N} titik untuk hierarchical clustering..."
            )
            rng = np.random.default_rng(42)
            sample_idx = rng.choice(N, HIER_MAX, replace=False)
            sample_coords = coords_radians[sample_idx]

            self.hierarchy_model.fit(sample_coords)
            sample_labels = self.hierarchy_model.labels_
            unique_labels = np.unique(sample_labels)

            centroids = np.vstack([
                sample_coords[sample_labels == k].mean(axis=0)
                for k in unique_labels
            ])

            dist = np.linalg.norm(
                coords_radians[:, np.newaxis, :] - centroids[np.newaxis, :, :],
                axis=2
            )
            hierarchy_labels = dist.argmin(axis=1)

        else:
            hierarchy_labels = self.hierarchy_model.fit_predict(
                coords_radians
            )

        is_anomaly = [
            True if x == -1 else False
            for x in anomalies
        ]

        df_processed['zona_klaster']    = clusters
        df_processed['hotspot_zone']    = hotspot_zones
        df_processed['hierarchy_label'] = hierarchy_labels
        df_processed['is_anomaly']      = is_anomaly

        print(
            f"Prediksi selesai untuk {len(df_processed)} data"
        )

        return df_processed