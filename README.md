# 🛡️ Anomaly-Based Intrusion Detection System (IDS)

A real-time, Machine Learning-powered Intrusion Detection System (IDS) built with Python. This project captures live network traffic, extracts features, and uses an Isolation Forest model to detect anomalous behavior (like port scans or sudden traffic bursts) instantly. It features a beautiful, dark-themed real-time web dashboard.

## 🚀 Features

- **Real-Time Packet Sniffing**: Uses `Scapy` to monitor live network interfaces.
- **Machine Learning Detection**: Uses `scikit-learn`'s Isolation Forest to establish a baseline of "normal" traffic and detect statistical outliers.
- **Dynamic Feature Extraction**: Processes traffic in rolling 1-second windows to calculate Packets per Second (PPS), Average Packet Size, TCP ratio, and UDP ratio.
- **Live Web Dashboard**: A premium, glassmorphism UI built with Flask, WebSockets (`flask-socketio`), and `Chart.js` to visualize traffic spikes and alert logs in real-time.

## 🛠️ Technology Stack

- **Backend / Core Logic**: Python, Scapy
- **Machine Learning**: Pandas, NumPy, Scikit-Learn
- **Web Server**: Flask, Flask-SocketIO (WebSockets)
- **Frontend**: HTML5, Vanilla CSS (Dark Mode/Glassmorphism), JavaScript, Chart.js

## 📂 Project Structure

```text
IDS_Project/
├── dashboard/               # Flask Web UI (HTML/CSS/JS)
├── data/                    # Training datasets (.csv)
├── logs/                    # Security alert logs
├── models/                  # Saved ML models (.pkl)
├── src/
│   ├── capture.py           # Network packet sniffer
│   ├── features.py          # Sliding-window feature extraction
│   ├── train.py             # ML model training logic
│   ├── detect.py            # Real-time anomaly prediction
│   └── alert.py             # Alert logging and system
├── main.py                  # Orchestrator script
├── requirements.txt         # Python dependencies
└── simulate_attack.py       # Safe testing script
```

## ⚙️ Installation & Setup

**Prerequisite (Windows Only)**: You must have [Npcap](https://npcap.com/) installed to capture raw network packets. (It is usually installed automatically if you have Wireshark on your PC).

1. **Clone the repository**
   ```bash
   git clone https://github.com/jayantshringi/Anomaly-Based-IDS.git
   cd Anomaly-Based-IDS
   ```

2. **Set up a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\Activate.ps1
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🚦 How to Use

### 1. Train the Model
Before the system can detect anomalies, it needs to learn what your "normal" traffic looks like. Browse the web normally (watch a video, scroll websites) while running this command:
```bash
python main.py --mode train --duration 60
```
This captures 60 seconds of baseline traffic and trains the Isolation Forest model.

### 2. Start the Live Dashboard
Start the real-time detector and the web server simultaneously:
```bash
python main.py --mode dashboard
```
Open your browser and navigate to `http://localhost:5000` to view the control center.

### 3. Simulate an Attack (Testing)
To verify the IDS works, open a second terminal and run the built-in attack simulation script (which performs a rapid local port scan):
```bash
python simulate_attack.py
```
Watch the web dashboard instantly detect the traffic spike and trigger the red alert warnings!

## ⚠️ Disclaimer
This project is intended for **educational and portfolio purposes only**. Never sniff or monitor networks that you do not own or do not have explicit permission to audit.
