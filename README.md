# Drone Communication Analysis System

## Overview

This project is a hybrid drone monitoring and analysis system designed for security research. It combines RF signal processing and network traffic analysis to detect, classify, and monitor drone communications in real time.

The system supports both SDR-based RF analysis and network-based monitoring using Viulinx modules, along with machine learning for traffic classification and a GUI dashboard for visualization. **(Currently Tested on Windows)**

---

## Features

- RF signal analysis (FFT-based)
- Frequency Hopping Spread Spectrum (FHSS) detection
- Network traffic capture using Wireshark/tshark
- Machine Learning-based traffic classification
- Protocol identification (heuristic-based)
- Real-time GUI dashboard (Tkinter)
- Packet inspector panel (live packet view)
- Start/Stop control system
- Signal strength detection (No Signal / Weak / Strong)
- Data logging for dataset creation

---

## System Architecture

### RF Pipeline
SDR / Simulated Input → FFT → Feature Extraction → ML Model → FHSS Detection → GUI

### Network Pipeline
Viulinx RX → Ethernet → Packet Capture (tshark) → Feature Extraction → ML Model → Protocol Detection → GUI

---

## Project Structure
```
drone_rf_analyzer/
│
├── main.py                  
├── config/                
│   ├── usb_detector.py 
|
├── hardware/              
│   ├── usb_detector.py    
│   └── sdr_interface.py    
│
├── signal_processing/      
│   ├── fft_processor.py   
│   ├── feature_extractor.py
│   ├── fhss_detector.py    
│   └── traffic_features.py 
│
├── ml/                     
│   ├── model.py           
│   ├── trainer.py          
│   ├── traffic_model.py    
│   └── traffic_trainer.py 
│
├── protocol/              
│   └── protocol_identifier.py
│
├── integration/           
│   ├── packet_capture.py  
│   └── wireshark_export.py 
│
├── gui/                   
│   ├── dashboard.py        
│   └── alerts.py           
│
└── utils/                  
    ├── logger.py          
    └── data_logger.py      
```
---

## Requirements

- Python 3.8+
- Wireshark (with tshark installed)
- Required Python packages: pip install pyshark scikit-learn numpy matplotlib

---

## Wireshark Setup

Ensure tshark is installed and accessible.

If installed in a custom location (e.g. D drive), 
  
    UPDATE: integration/packet_capture.py
    Set: TSHARK_PATH = r"D:\Wireshark\tshark.exe" //Whatever your PATH is

Verify installation:

    tshark -v

---

## Running the System

### Basic Run
    python main.py

---

### Using CLI Arguments
    python main.py --mode HYBRID --interface Ethernet

---

### Available Modes

| Mode | Description |
|------|------------|
| RF | RF signal analysis only |
| NETWORK | Network traffic analysis only |
| HYBRID | Both RF and network |

---

## GUI Dashboard

The GUI provides:

- RF classification output
- Network traffic classification
- Protocol identification
- Signal strength indicator
- Packet inspector (live packet summaries)
- Alerts panel
- Start / Stop controls

---

## Signal Status Indicators

| Status | Condition |
|------|----------|
| NO SIGNAL | No RF power / no packets |
| WEAK SIGNAL | Low activity |
| STRONG / ACTIVE | High signal or traffic |

---

## Machine Learning

### Model Used
- Random Forest Classifier

### Input Features

#### RF
- Bandwidth
- Power
- Variance

#### Network
- Packet rate
- Average packet size
- Packet interval

### Output Classes
- Video traffic
- Control signals
- Telemetry
- Noise

---

## Data Logging

All processed data is stored in:
session_log.json //it will be created automatically after first use

This can be used to:
- build datasets
- retrain ML models
- perform offline analysis

---

## Known Limitations

- Cannot decode encrypted communication
- RF analysis requires SDR hardware for real signals
- ML model uses synthetic data (needs real dataset for accuracy)
- PyShark may require manual configuration on Windows

---

## Troubleshooting

### tshark not found
Ensure correct path is set in packet_capture.py

### No packets captured
- Check correct network interface (`tshark -D`)
- Ensure device is connected
- Run with admin privileges

### USB backend error
Install libusb drivers using Zadig (if using SDR)

---

## Future Enhancements

- Real dataset training pipeline
- Advanced ML models (XGBoost, Deep Learning)
- Direction finding (localization)
- Multi-node distributed detection
- Drone signature database
- Real-time waterfall visualization
- GUI upgrade (PyQt)

---

## Disclaimer

This project is intended for educational and research purposes only. All implementations are based on theoretical models and controlled experimentation. Real-world behavior may vary due to hardware limitations, environmental conditions, and protocol-specific protections such as encryption and authentication.

---

## Key Insight

This system combines:

- RF intelligence (signal-level)
- Network intelligence (packet-level)
