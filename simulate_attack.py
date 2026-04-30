import socket
import threading
import time

def scan_port(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.1) # Fast timeout for quick scanning
        s.connect(('127.0.0.1', port))
        s.close()
    except:
        pass

def simulate_port_scan():
    print("🚀 Starting simulated port scan against localhost...")
    start_time = time.time()
    
    threads = []
    # Scan first 1000 ports quickly to trigger the IDS
    for port in range(1, 1001):
        t = threading.Thread(target=scan_port, args=(port,))
        threads.append(t)
        t.start()
        
        # Slight delay to control the burst rate
        time.sleep(0.002) 
        
    for t in threads:
        t.join()
        
    print(f"✅ Simulated attack finished in {time.time() - start_time:.2f} seconds.")

if __name__ == "__main__":
    simulate_port_scan()
