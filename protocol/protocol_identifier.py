def identify_protocol(features):
    avg_size = features["avg_size"]
    rate = features["packet_rate"]
    interval = features["avg_interval"]

    # Heuristic rules
    if avg_size > 800 and rate > 50:
        return "Likely OFDM (WiFi-based Drone Link)"

    elif rate < 20 and interval > 0.05:
        return "Telemetry Protocol (Low bandwidth)"

    elif rate > 20 and interval < 0.02:
        return "Control Link (RC / FHSS-like behavior)"

    else:
        return "Unknown / Mixed Traffic"