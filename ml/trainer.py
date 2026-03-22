import numpy as np

def generate_training_data():
    X = []
    y = []

    for _ in range(200):
        bw = np.random.randint(10, 300)
        power = np.random.uniform(0, 100)
        var = np.random.uniform(0, 50)

        X.append([bw, power, var])

        if bw > 200:
            y.append("WiFi/Drone")
        elif 50 < bw <= 200:
            y.append("FHSS/RC")
        else:
            y.append("Telemetry")

    return X, y