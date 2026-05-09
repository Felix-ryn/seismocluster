# filepath: backend/app/models/clustering/kmeans_model.py
from sklearn.cluster import KMeans
import numpy as np
import joblib
import os

class KMeansClustering:
    def __init__(self, n_clusters: int = 5):
        # Menggunakan 5 cluster sebagai baseline untuk area Indonesia
        self.model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        self.model_path = os.path.join(os.path.dirname(__file__), '../saved_models/kmeans_model.joblib')

    def run(self, features: np.ndarray) -> np.ndarray:
        """melatih data, mengembalikan label, dan menyimpan model ke disk."""
        labels = self.model.fit_predict(features)
        self._save_model()
        return labels
    
    def _save_model(self):
        """Menyimpan model ke dalam fomat file .joblib"""
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump(self.model, self.model_path)
        print(f"K-Means model saved to {self.model_path}")
    
    def predict_realtime(self, new_features: np.ndarray) -> np.ndarray:
        """untuk memprediksi cluster dari data baru menggunakan model yang sudah dilatih."""
        if not os.path.exists(self.model_path):
            raise FileNotFoundError("Model K-Means belum ada! Jalankan pipeline utama terlebih dahulu.")
        loaded_model = joblib.load(self.model_path)
        return loaded_model.predict(new_features)