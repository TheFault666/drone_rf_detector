import usb.core
import usb.backend.libusb1

def list_devices():
    backend = usb.backend.libusb1.get_backend()

    if backend is None:
        print("[WARNING] No USB backend found (libusb missing)")
        return []

    devices = usb.core.find(find_all=True, backend=backend)

    found = []
    for dev in devices:
        try:
            vid = hex(dev.idVendor)
            pid = hex(dev.idProduct)
            found.append((vid, pid))
        except:
            continue

    return found


def detect_sdr():
    devices = list_devices()

    if not devices:
        print("[INFO] No USB devices or backend not available")
        return []

    return devices