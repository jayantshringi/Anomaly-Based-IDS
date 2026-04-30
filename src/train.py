import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
import os
import logging

def train_model(data_path, model_save_path):
    logging.info(f"Loading training data from {data_path}")
    if not os.path.exists(data_path):
        logging.error(f"Data file {data_path} not found.")
        return False
        
    df = pd.read_csv(data_path)
    if len(df) < 10:
        logging.error("Not enough data to train. Need at least 10 samples.")
        return False
        
    # Assuming columns: pps, avg_size, tcp_ratio, udp_ratio
    X = df.values
    
    logging.info("Training Isolation Forest model...")
    # contamination is the proportion of outliers in the data set
    # Using a small value since training data should be normal
    model = IsolationForest(contamination=0.01, random_state=42)
    model.fit(X)
    
    os.makedirs(os.path.dirname(model_save_path), exist_ok=True)
    joblib.dump(model, model_save_path)
    logging.info(f"Model saved to {model_save_path}")
    return True
