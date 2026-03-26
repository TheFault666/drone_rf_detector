import json
import time
import numpy as np

def convert_numpy(obj):
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.bool_):   # ✅ ADD THIS LINE
        return bool(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    return obj

def log_data(data, filename="session_log.json"):
    data["timestamp"] = time.time()

    clean_data = {}

    for k, v in data.items():
        if isinstance(v, dict):
            clean_data[k] = {kk: convert_numpy(vv) for kk, vv in v.items()}
        else:
            clean_data[k] = convert_numpy(v)

    with open(filename, "a") as f:
        f.write(json.dumps(clean_data) + "\n")