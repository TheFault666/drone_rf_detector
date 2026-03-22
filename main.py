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
import numpy as np

# Setup
log("Starting system...")

# Detect hardware
devices = detect_sdr()
log(f"Detected SDRs: {devices}")

# Train model
X, y = generate_training_data()
model = RFModel()
model.train(X, y)

fhss = FHSSDetector()
wf = Waterfall()

# Main loop
for _ in range(50):
    samples = get_samples()
    power = compute_fft(samples)

    features = extract_features(power)
    prediction = model.predict([
        features["bandwidth"],
        features["power"],
        features["variance"]
    ])

    peaks = np.where(power > np.mean(power))[0]
    hopping = fhss.detect(peaks)

    log(f"Prediction: {prediction}")
    if hopping:
        log("FHSS detected")

    wf.update(power)
    wf.show()

    export_to_json({
        "features": features,
        "prediction": prediction,
        "fhss": hopping
    })