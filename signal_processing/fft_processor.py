import numpy as np
from config.settings import FFT_SIZE

def compute_fft(samples):
    spectrum = np.fft.fftshift(np.fft.fft(samples, FFT_SIZE))
    power = 20 * np.log10(np.abs(spectrum))
    return power