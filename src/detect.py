import joblib
import os
import logging
import numpy as np

class AnomalyDetector:
    def __init__(self, model_path):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}. Please train the model first.")
        self.model = joblib.load(model_path)
        logging.info("Model loaded successfully.")
        
    def predict(self, features):
        # features is a list like [pps, avg_size, tcp_ratio, udp_ratio]
        X = np.array(features).reshape(1, -1)
        prediction = self.model.predict(X)
        return prediction[0] # Returns 1 for normal, -1 for anomaly
