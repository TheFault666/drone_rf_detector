import tkinter as tk

class Dashboard:
    def __init__(self, start_callback=None, stop_callback=None):
        self.root = tk.Tk()
        self.root.title("Drone Monitoring System")
        self.start_btn = tk.Button(self.root, text="Start", command=start_callback, bg="green")
        self.start_btn.pack()

        self.stop_btn = tk.Button(self.root, text="Stop", command=stop_callback, bg="red")
        self.stop_btn.pack()

        self.packet_box = tk.Text(self.root, height=15, width=80)
        self.packet_box.pack()
        self.packet_rate = tk.Label(self.root, text="Packet Rate: 0")
        self.packet_rate.pack()

        # Labels
        self.rf_label = tk.Label(self.root, text="RF Status: N/A")
        self.rf_label.pack()
        self.rf_power = tk.Label(self.root, text="RF Power: 0")
        self.rf_power.pack()

        self.net_label = tk.Label(self.root, text="Network Status: N/A")
        self.net_label.pack()

        self.alert_label = tk.Label(self.root, text="Alerts: None", fg="red")
        self.alert_label.pack()

        self.signal_status = tk.Label(self.root, text="Signal: UNKNOWN", fg="blue")
        self.signal_status.pack()

    def update_rf_power(self, value):
        self.rf_power.config(text=f"RF Power: {value:.2f}")

    def update_packet_rate(self, value):
        self.packet_rate.config(text=f"Packet Rate: {value}")

    def update_packets(self, packets):
        self.packet_box.delete("1.0", tk.END)

        for pkt in packets[:10]:  # show only 10
            try:
                summary = f"{pkt.sniff_time} | {pkt.highest_layer} | {pkt.length}\n"
                self.packet_box.insert(tk.END, summary)
            except:
                continue
    
    def update_signal_status(self, status):
        color = "green"

        if status == "NO SIGNAL":
            color = "red"
        elif status == "WEAK SIGNAL":
            color = "orange"

        self.signal_status.config(text=f"Signal: {status}", fg=color)

    def update_rf(self, text):
        self.rf_label.config(text=f"RF: {text}")

    def update_net(self, text):
        self.net_label.config(text=f"Network: {text}")

    def update_alerts(self, alerts):
        if alerts:
            self.alert_label.config(text="ALERT: " + ", ".join(alerts))
        else:
            self.alert_label.config(text="Alerts: None")

    def run(self):
        self.root.mainloop()