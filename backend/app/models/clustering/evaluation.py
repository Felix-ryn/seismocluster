# filepath: backend/app/models/clustering/evaluation.py
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
import numpy as np

class ClusterEvaluator:
    @staticmethod
    def evaluate_model(model_name: str, features: np.ndarray, labels: np.ndarray) -> dict:
        """
        Menghitung 3 metrik validasi clustering secara profesional.
        - Silhouette: Kerapatan cluster (Mendekati 1 lebih baik).
        - Davies-Bouldin: Jarak antar cluster (Mendekati 0 lebih baik).
        - Calinski-Harabasz: Rasio dispersi (Semakin tinggi semakin baik).
        """
        unique_labels = np.unique(labels)
        
        # Penanganan Error: Jika algoritma (seperti DBSCAN) hanya menemukan 1 cluster atau semuanya noise
        if len(unique_labels) < 2 or (len(unique_labels) == 2 and -1 in unique_labels):
            return {
                "model": model_name,
                "silhouette_score": 0.0,
                "davies_bouldin_index": 0.0,
                "calinski_harabasz_score": 0.0,
                "status": "Warning: Hanya terbentuk 1 cluster relevan atau dominan noise."
            }

        # Menghitung metrik jika cluster valid
        return {
            "model": model_name,
            "silhouette_score": round(float(silhouette_score(features, labels)), 4),
            "davies_bouldin_index": round(float(davies_bouldin_score(features, labels)), 4),
            "calinski_harabasz_score": round(float(calinski_harabasz_score(features, labels)), 4),
            "status": "Success"
        }