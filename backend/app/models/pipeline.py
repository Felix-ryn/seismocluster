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
            "SeismoCluster_Clustering_Model_KMeans"
        )

        self.hotspot_model_name = os.getenv(
            "MLFLOW_HOTSPOT_MODEL_NAME",
            "SeismoCluster_Hotspot_Model"
        )

        self.anomaly_model_name = os.getenv(
            "MLFLOW_ANOMALY_MODEL_NAME",
            "SeismoCluster_Anomaly_Model_ISF"
        )

        self.hierarchy_model_name = os.getenv(
            "MLFLOW_HIERARCHY_MODEL_NAME",
            "SeismoCluster_Hierarchy_Model"
        )

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
                f"Load Hotspot Model: {self.hotspot_model_name}"
            )
            self.hotspot_model = mlflow.sklearn.load_model(
                f"models:/{self.hotspot_model_name}@champion"
            )

            print(
                f"Load Anomaly Model: {self.anomaly_model_name}"
            )
            self.anomaly_model = mlflow.sklearn.load_model(
                f"models:/{self.anomaly_model_name}@champion"
            )

            print(
                f"Load Hierarchy Model: {self.hierarchy_model_name}"
            )
            self.hierarchy_model = mlflow.sklearn.load_model(
                f"models:/{self.hierarchy_model_name}@champion"
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
            self.hotspot_model    is None or
            self.anomaly_model    is None or
            self.hierarchy_model  is None
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

        # Gunakan .values agar model tidak sensitif terhadap nama kolom
        coords_radians = df_processed[
            ['lat_radian', 'lon_radian']
        ].values

        # ==========================================
        # DATA 4D ANOMALY
        # ==========================================
        # .values agar tidak memicu warning feature names pada IsolationForest
        X_anomaly = df_processed[
            [
                'latitude_scaled',
                'longitude_scaled',
                'depth_scaled',
                'magnitude_scaled'
            ]
        ].values

        # ==========================================
        # KMEANS CLUSTERING
        # ==========================================
        print(
            "Menjalankan KMeans clustering..."
        )

        clusters = self.clustering_model.predict(
            coords_radians
        )

        # ==========================================
        # RELABEL CLUSTERS — barat → timur (konsisten lintas training)
        # KMeans menghasilkan label arbitrary; sort by mean longitude
        # agar Cluster 0 selalu region paling barat, dst.
        # ==========================================
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

        # ==========================================
        # HOTSPOT DETECTION
        # Hotspot model (DBSCAN Haversine) butuh
        # koordinat radian 2D: [lat_rad, lon_rad]
        # ==========================================
        print(
            "Menjalankan hotspot detection..."
        )

        hotspot_zones = self.hotspot_model.fit_predict(
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
        # HIERARCHICAL CLUSTERING
        # Ward linkage is O(n²) memory — subsample large datasets,
        # then assign all points to nearest cluster centroid.
        # ==========================================
        print(
            "Menjalankan hierarchical clustering..."
        )

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

            # Centroid per cluster dari sample
            centroids = np.vstack([
                sample_coords[sample_labels == k].mean(axis=0)
                for k in unique_labels
            ])

            # Assign semua titik ke centroid terdekat
            dist = np.linalg.norm(
                coords_radians[:, np.newaxis, :] - centroids[np.newaxis, :, :],
                axis=2
            )
            hierarchy_labels = dist.argmin(axis=1)

        else:
            hierarchy_labels = self.hierarchy_model.fit_predict(
                coords_radians
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
        df_processed['zona_klaster']   = clusters
        df_processed['hotspot_zone']   = hotspot_zones
        df_processed['hierarchy_label'] = hierarchy_labels
        df_processed['is_anomaly']     = is_anomaly

        print(
            f"Prediksi selesai untuk {len(df_processed)} data"
        )

        return df_processed