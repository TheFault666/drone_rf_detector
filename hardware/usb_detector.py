import usb.core
from config.settings import SDR_DEVICES

def list_devices():
    devices = usb.core.find(find_all=True)
    found = []

    for dev in devices:
        vid = hex(dev.idVendor)
        pid = hex(dev.idProduct)

        found.append((vid, pid))

    return found

def detect_sdr():
    devices = list_devices()

    detected = []
    for d in devices:
        if d in SDR_DEVICES:
            detected.append(SDR_DEVICES[d])

    return detected