import numpy as np

def generate_training_data():
    X = []
    y = []

    for _ in range(300):
        avg_size = np.random.randint(50, 1500)
        rate = np.random.randint(5, 100)
        interval = np.random.uniform(0.001, 0.1)

        X.append([avg_size, rate, interval])

        if avg_size > 800 and rate > 50:
            y.append("Video")
        elif rate < 20:
            y.append("Telemetry")
        else:
            y.append("Control")

    return X, y