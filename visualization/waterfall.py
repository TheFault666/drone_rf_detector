import matplotlib.pyplot as plt
import numpy as np
from collections import deque

class Waterfall:
    def __init__(self, size=100):
        self.buffer = deque(maxlen=size)

    def update(self, power):
        self.buffer.append(power)

    def show(self):
        plt.imshow(np.array(self.buffer), aspect='auto', origin='lower')
        plt.pause(0.01)