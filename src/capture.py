import logging
from scapy.all import sniff, IP

def packet_callback(packet, packet_queue):
    # Pass the packet to the queue for feature extraction
    if IP in packet:
        packet_queue.append(packet)

def start_capture(interface, packet_queue, stop_event):
    logging.info(f"Starting packet capture. Interface: {interface if interface else 'Default'}")
    try:
        # Sniff packets until stop_event is set
        if interface:
            sniff(iface=interface, prn=lambda pkt: packet_callback(pkt, packet_queue), 
                  store=False, stop_filter=lambda p: stop_event.is_set())
        else:
            sniff(prn=lambda pkt: packet_callback(pkt, packet_queue), 
                  store=False, stop_filter=lambda p: stop_event.is_set())
    except Exception as e:
        logging.error(f"Error during capture: {e}")
