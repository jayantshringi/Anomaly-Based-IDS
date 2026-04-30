import argparse
import threading
import time
import os
import csv
import logging
from src.capture import start_capture
from src.features import FeatureExtractor
from src.detect import AnomalyDetector
from src.alert import AlertSystem
from src.train import train_model

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def train_mode(interface, data_path, duration):
    print(f"Starting training data collection on interface: {interface if interface else 'Default'} for {duration} seconds...")
    packet_queue = []
    stop_event = threading.Event()
    
    capture_thread = threading.Thread(target=start_capture, args=(interface, packet_queue, stop_event))
    capture_thread.daemon = True
    capture_thread.start()
    
    extractor = FeatureExtractor(window_size=1.0)
    
    os.makedirs(os.path.dirname(data_path), exist_ok=True)
    with open(data_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['pps', 'avg_size', 'tcp_ratio', 'udp_ratio'])
        
        start_time = time.time()
        while time.time() - start_time < duration:
            if packet_queue:
                packet = packet_queue.pop(0)
                features = extractor.process_packet(packet)
                if features:
                    writer.writerow(features)
                    f.flush()
                    print(f"Collected normal sample: [pps: {features[0]:.2f}, avg_size: {features[1]:.2f}, tcp: {features[2]:.2f}, udp: {features[3]:.2f}]")
            else:
                time.sleep(0.01)
                
    stop_event.set()
    capture_thread.join(timeout=2)
    print("\nData collection finished. Training model...")
    
    train_model(data_path, "models/isolation_forest.pkl")

def detect_mode(interface, model_path, on_alert=None, on_traffic=None):
    print(f"Starting real-time anomaly detection on interface: {interface if interface else 'Default'}...")
    packet_queue = []
    stop_event = threading.Event()
    
    try:
        detector = AnomalyDetector(model_path)
    except FileNotFoundError as e:
        print(f"\033[91mError: {e}\033[0m")
        return
        
    alert_sys = AlertSystem("logs", on_alert=on_alert)
    extractor = FeatureExtractor(window_size=1.0)
    
    capture_thread = threading.Thread(target=start_capture, args=(interface, packet_queue, stop_event))
    capture_thread.daemon = True
    capture_thread.start()
    
    print("Monitoring traffic... Press Ctrl+C to stop.")
    try:
        while True:
            if packet_queue:
                packet = packet_queue.pop(0)
                features = extractor.process_packet(packet)
                if features:
                    prediction = detector.predict(features)
                    
                    if on_traffic:
                        on_traffic(features)
                        
                    if prediction == -1:
                        alert_sys.trigger_alert(features)
                    else:
                        print(f"Normal traffic window. | pps: {features[0]:.2f} | avg_size: {features[1]:.2f}", end='\r')
            else:
                time.sleep(0.01)
    except KeyboardInterrupt:
        print("\nStopping detection...")
        stop_event.set()
        capture_thread.join(timeout=2)

def dashboard_mode(interface, model_path):
    from dashboard.app import start_dashboard, socketio
    
    def on_alert(features):
        socketio.emit('new_alert', {'pps': features[0], 'avg_size': features[1], 'tcp_ratio': features[2], 'udp_ratio': features[3]})
        
    def on_traffic(features):
        socketio.emit('traffic_update', {'pps': features[0], 'avg_size': features[1]})
        
    print(f"\n🚀 Starting Real-Time IDS Dashboard...")
    print(f"🌐 Web UI will be available at http://localhost:5000\n")
    
    # Start detection in background thread
    detect_thread = threading.Thread(target=detect_mode, args=(interface, model_path, on_alert, on_traffic))
    detect_thread.daemon = True
    detect_thread.start()
    
    # Start web server on main thread
    start_dashboard(port=5000)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Anomaly-Based Intrusion Detection System")
    parser.add_argument('--mode', choices=['train', 'detect', 'dashboard'], required=True, help="Run mode: train, detect, or dashboard")
    parser.add_argument('--interface', required=False, default=None, help="Network interface to sniff (e.g., Wi-Fi, eth0, or let Scapy choose)")
    parser.add_argument('--duration', type=int, default=30, help="Duration in seconds for training data collection")
    
    args = parser.parse_args()
    
    if args.mode == 'train':
        train_mode(args.interface, "data/normal_traffic.csv", args.duration)
    elif args.mode == 'detect':
        detect_mode(args.interface, "models/isolation_forest.pkl")
    elif args.mode == 'dashboard':
        dashboard_mode(args.interface, "models/isolation_forest.pkl")
