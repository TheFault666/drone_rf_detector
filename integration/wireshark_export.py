import json

def export_to_json(data, filename="rf_capture.json"):
    with open(filename, "a") as f:
        f.write(json.dumps(data) + "\n")