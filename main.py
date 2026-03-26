from hardware.usb_detector import detect_sdr
from hardware.sdr_interface import get_samples
from signal_processing.fft_processor import compute_fft
from signal_processing.feature_extractor import extract_features
from signal_processing.fhss_detector import FHSSDetector
from ml.model import RFModel
from ml.trainer import generate_training_data
from visualization.waterfall import Waterfall
from integration.wireshark_export import export_to_json
from utils.logger import log
import argparse
import numpy as np
from integration.packet_capture import capture_packets
from signal_processing.traffic_features import extract_packet_features
from ml.traffic_model import TrafficModel
from ml.traffic_trainer import generate_training_data as traffic_data
from protocol.protocol_identifier import identify_protocol
from utils.logger import log
from gui.dashboard import Dashboard
from gui.plots import LivePlot
from gui.alerts import check_alerts
from utils.data_logger import log_data
import time
import threading
from gui.alerts import check_alerts

# ---------------- CONFIG ----------------
parser = argparse.ArgumentParser(
    description="Drone Communication Analysis System"
)

parser.add_argument(
    "--mode",
    choices=["RF", "NETWORK", "HYBRID"],
    default="HYBRID",
    help="Select operation mode"
)

parser.add_argument(
    "--interface",
    default="Ethernet",
    help="Network interface for packet capture"
)

args = parser.parse_args()

MODE = args.mode
INTERFACE = args.interface


log("Starting system...")

# Detect hardware
devices = detect_sdr()
log(f"Detected SDRs: {devices}")

# ---------------- RF MODEL ----------------
X, y = generate_training_data()
rf_model = RFModel()
rf_model.train(X, y)

fhss = FHSSDetector()
wf = Waterfall()

# ---------------- NETWORK MODEL ----------------
X_t, y_t = traffic_data()
traffic_model = TrafficModel()
traffic_model.train(X_t, y_t)

#----------Global Control Flag------------
RUNNING = False

# ---------------- MAIN LOOP ----------------
def run_system():
    global RUNNING

    while RUNNING:
        print("\n==============================")

        rf_data = None
        net_data = None

        # ---------------- RF ----------------
        if MODE in ["RF", "HYBRID"]:
            samples = get_samples()
            power = compute_fft(samples)

            rf_features = extract_features(power)
            power_val = float(rf_features["power"])

            if power_val < 5:
                signal_status = "NO SIGNAL"
            elif power_val < 20:
                signal_status = "WEAK SIGNAL"
            else:
                signal_status = "STRONG SIGNAL"

            rf_prediction = rf_model.predict([
                rf_features["bandwidth"],
                rf_features["power"],
                rf_features["variance"]
            ])

            peaks = np.where(power > np.mean(power))[0]
            hopping = fhss.detect(peaks)

            rf_data = {
                "power": rf_features["power"],
                "fhss": hopping
            }

            dashboard.root.after(0, dashboard.update_rf, rf_prediction)
            dashboard.root.after(0, dashboard.update_rf_power, rf_features["power"])
            dashboard.root.after(0, dashboard.update_signal_status, signal_status)

            log_data({
                "type": "rf",
                "features": rf_features,
                "prediction": rf_prediction,
                "fhss": hopping
            })

        # ---------------- NETWORK ----------------
        if MODE in ["NETWORK", "HYBRID"]:
            packets = capture_packets(interface=INTERFACE, packet_count=20)

            net_features = extract_packet_features(packets)

            rate = net_features.get("packet_rate", 0)

            if rate == 0:
                net_status = "NO SIGNAL"
            elif rate < 10:
                net_status = "WEAK SIGNAL"
            else:
                net_status = "ACTIVE SIGNAL"

            dashboard.root.after(0, dashboard.update_signal_status, net_status)

            if net_features:
                net_prediction = traffic_model.predict([
                    net_features["avg_size"],
                    net_features["packet_rate"],
                    net_features["avg_interval"]
                ])

                protocol = identify_protocol(net_features)

                net_data = net_features

                dashboard.update_net(f"{net_prediction} | {protocol}")
                dashboard.update_packet_rate(net_features["packet_rate"])

                # 👉 ADD THIS LINE (Packet Inspector)
                dashboard.update_packets(packets)

                log_data({
                    "type": "network",
                    "features": net_features,
                    "prediction": net_prediction,
                    "protocol": protocol
                })

        # ---------------- ALERTS ----------------
        alerts = check_alerts(rf_data, net_data)
        dashboard.update_alerts(alerts)

        time.sleep(1)

def start_system():
    global RUNNING
    if not RUNNING:
        RUNNING = True
        threading.Thread(target=run_system, daemon=True).start()

def stop_system():
    global RUNNING
    RUNNING = False

#----------------Dashboard init-----------------
dashboard = Dashboard(start_callback=start_system, stop_callback=stop_system)
dashboard.run()