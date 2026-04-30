import logging
import os
from datetime import datetime

class AlertSystem:
    def __init__(self, log_dir, on_alert=None):
        os.makedirs(log_dir, exist_ok=True)
        self.log_file = os.path.join(log_dir, 'alerts.log')
        self.on_alert = on_alert
        
        # Configure file logging
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        file_handler.setFormatter(formatter)
        
        self.logger = logging.getLogger('AlertSystem')
        self.logger.setLevel(logging.INFO)
        # Avoid duplicate logs if instantiated multiple times
        if not self.logger.handlers:
            self.logger.addHandler(file_handler)
                            
    def trigger_alert(self, features):
        pps, avg_size, tcp_ratio, udp_ratio = features
        msg = f"Suspicious traffic detected! | pps: {pps:.2f} | avg_size: {avg_size:.2f} | tcp_ratio: {tcp_ratio:.2f} | udp_ratio: {udp_ratio:.2f}"
        
        # Red text in console
        print(f"\n\033[91m⚠️ ALERT: {msg}\033[0m") 
        
        # Log to file
        self.logger.info(msg)
        
        # Trigger external callback
        if self.on_alert:
            self.on_alert(features)
