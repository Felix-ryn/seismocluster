from sklearn.ensemble import IsolationForest
import numpy as np
import joblib
import os

class IsolationForestAnomaly:
    def __init__(self, contamination: float = 0.01):
        # contamination = 0.01 berarti kita berasumsi hanya 1% dari total gempa yang merupakan anomali ekstrem
        self.model = IsolationForest(
            n_estimators=100, 
            contamination=contamination, 
            random_state=42
        )
        self.model_path = os.path.join(os.path.dirname(__file__), '../../saved_models/iforest_model.joblib')
        
    def run(self, features: np.ndarray) -> np.ndarray:
        """
        Melatih model dan mendeteksi anomali.
        Output asli Isolation Forest: 1 (Normal), -1 (Anomali).
        Fungsi ini mengubahnya menjadi boolean (True untuk Anomali, False untuk Normal) agar mudah diolah.
        """
        predictions = self.model.fit_predict(features)
        self._save_model()
        return predictions == -1
    
    def _save_model(self):
        """menyimmpan model ke dalam format file .joblib"""
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump(self.model, self.model_path)
        print("Model Isolation Forest berhasil disimpan ke disk.")