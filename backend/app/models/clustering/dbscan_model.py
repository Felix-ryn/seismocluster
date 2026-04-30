# filepath: backend/app/models/clustering/dbscan_model.py
from sklearn.cluster import DBSCAN
import numpy as np

class DBSCANClustering:
    def __init__(self, eps: float = 0.15, min_samples: int = 15):
        # Parameter hasil tuning untuk data koordinat yang sudah di-scale
        self.model = DBSCAN(eps=eps, min_samples=min_samples)

    def run(self, features: np.ndarray) -> np.ndarray:
        """
        Mengembalikan label cluster.
        Nilai -1 adalah NOISE (gempa terpencil). Nilai >= 0 adalah HOTSPOT.
        """
        return self.model.fit_predict(features)