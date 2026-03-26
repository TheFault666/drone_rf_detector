def check_alerts(rf_data=None, net_data=None):
    alerts = []

    # RF alerts
    if rf_data:
        if rf_data.get("fhss"):
            alerts.append("FHSS signal detected")

        if rf_data.get("power", 0) > 80:
            alerts.append("High RF power detected")

    # Network alerts
    if net_data:
        if net_data["packet_rate"] > 80:
            alerts.append("High traffic rate")

        if net_data["avg_interval"] < 0.005:
            alerts.append("Burst traffic detected")

    return alerts