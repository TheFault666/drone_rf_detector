import pyshark
import asyncio

TSHARK_PATH = r"<Path>\tshark.exe"

def capture_packets(interface="Ethernet", packet_count=20):
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        cap = pyshark.LiveCapture(
            interface=interface,
            tshark_path=TSHARK_PATH
        )

        packets = []
        for pkt in cap.sniff_continuously(packet_count=packet_count):
            packets.append(pkt)

        return packets

    except Exception as e:
        print(f"[NET ERROR] {e}")
        return []
