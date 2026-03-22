import numpy as np
from config.settings import HOP_THRESHOLD

class FHSSDetector:
    def __init__(self):
        self.prev_peaks = None

    def detect(self, peaks):
        if self.prev_peaks is None or len(peaks) == 0:
            self.prev_peaks = peaks
            return False

        shifts = [abs(p - q) for p, q in zip(peaks, self.prev_peaks)]
        avg_shift = np.mean(shifts) if shifts else 0

        self.prev_peaks = peaks

        return avg_shift > HOP_THRESHOLD