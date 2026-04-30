# filepath: backend/app/models/clustering/kmeans_model.py
from sklearn.cluster import KMeans
import numpy as np

class KMeansClustering:
    def __init__(self, n_clusters: int = 5):
        # Menggunakan 5 cluster sebagai baseline untuk area Indonesia
        self.model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)

    def run(self, features: np.ndarray) -> np.ndarray:
        """Menerima array fitur dan mengembalikan label cluster (0, 1, 2, ...)."""
        return self.model.fit_predict(features)