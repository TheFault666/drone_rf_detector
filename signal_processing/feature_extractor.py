import numpy as np

def extract_features(power):
    bandwidth = np.sum(power > np.mean(power))
    peak_power = np.max(power)
    variance = np.var(power)

    return {
        "bandwidth": bandwidth,
        "power": peak_power,
        "variance": variance
    }