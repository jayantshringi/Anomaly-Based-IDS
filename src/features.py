import time
from scapy.all import IP, TCP, UDP

class FeatureExtractor:
    def __init__(self, window_size=1.0):
        self.window_size = window_size
        self.current_window_start = time.time()
        self.packet_count = 0
        self.total_size = 0
        self.protocol_counts = {'TCP': 0, 'UDP': 0, 'Other': 0}
        
    def process_packet(self, packet):
        if IP not in packet:
            return None
            
        current_time = time.time()
        
        # Check if window is over BEFORE processing current packet
        if current_time - self.current_window_start >= self.window_size:
            # Calculate features for the past window
            features = self._calculate_features()
            self._reset_window(current_time)
            
            # Now process the current packet in the new window
            self._add_packet(packet)
            return features
        else:
            # Add to current window
            self._add_packet(packet)
            return None
            
    def _add_packet(self, packet):
        size = len(packet)
        self.total_size += size
        self.packet_count += 1
        
        if TCP in packet:
            self.protocol_counts['TCP'] += 1
        elif UDP in packet:
            self.protocol_counts['UDP'] += 1
        else:
            self.protocol_counts['Other'] += 1
        
    def _calculate_features(self):
        pps = self.packet_count / self.window_size
        avg_size = self.total_size / self.packet_count if self.packet_count > 0 else 0
        tcp_ratio = self.protocol_counts['TCP'] / self.packet_count if self.packet_count > 0 else 0
        udp_ratio = self.protocol_counts['UDP'] / self.packet_count if self.packet_count > 0 else 0
        
        # [Packets/sec, Avg packet size, TCP ratio, UDP ratio]
        return [pps, avg_size, tcp_ratio, udp_ratio]
        
    def _reset_window(self, current_time):
        self.current_window_start = current_time
        self.packet_count = 0
        self.total_size = 0
        self.protocol_counts = {'TCP': 0, 'UDP': 0, 'Other': 0}
