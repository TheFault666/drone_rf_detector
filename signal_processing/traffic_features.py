def extract_packet_features(packets):
    sizes = []
    intervals = []

    prev_time = None

    for pkt in packets:
        try:
            size = int(pkt.length)
            time = float(pkt.sniff_timestamp)

            sizes.append(size)

            if prev_time:
                intervals.append(time - prev_time)

            prev_time = time
        except:
            continue

    if not sizes:
        return None

    return {
        "avg_size": sum(sizes) / len(sizes),
        "max_size": max(sizes),
        "packet_rate": len(packets),
        "avg_interval": sum(intervals)/len(intervals) if intervals else 0
    }