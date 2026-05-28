from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
import numpy as np

class ClusterEvaluator:
    @staticmethod
    def evaluate_model(model_name: str, features: np.ndarray, labels: np.ndarray) -> dict:
        """
        Menghitung 3 metrik validasi clustering.
        - Silhouette: Kerapatan cluster (Mendekati 1 lebih baik).
        - Davies-Bouldin: Jarak antar cluster (Mendekati 0 lebih baik).
        - Calinski-Harabasz: Rasio dispersi (Semakin tinggi semakin baik).
        Label -1 (noise dari DBSCAN) dihapus sebelum evaluasi.
        """
        labels = np.array(labels)
        features = np.array(features)

        # Buang noise points (-1) dari DBSCAN sebelum evaluasi
        mask = labels != -1
        clean_labels = labels[mask]
        clean_features = features[mask]

        unique_labels = np.unique(clean_labels)

        # Butuh minimal 2 cluster dan minimal 2 sampel per cluster
        if len(unique_labels) < 2:
            return {
                "model": model_name,
                "silhouette_score": 0.0,
                "davies_bouldin_index": 0.0,
                "calinski_harabasz_score": 0.0,
                "status": "Warning: Kurang dari 2 cluster valid terbentuk."
            }

        try:
            return {
                "model": model_name,
                "silhouette_score": round(float(silhouette_score(clean_features, clean_labels)), 4),
                "davies_bouldin_index": round(float(davies_bouldin_score(clean_features, clean_labels)), 4),
                "calinski_harabasz_score": round(float(calinski_harabasz_score(clean_features, clean_labels)), 4),
                "status": "Success"
            }
        except Exception as e:
            return {
                "model": model_name,
                "silhouette_score": 0.0,
                "davies_bouldin_index": 0.0,
                "calinski_harabasz_score": 0.0,
                "status": f"Error saat evaluasi: {str(e)}"
            }