import zmq
import numpy as np

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5555")

def stream_data(data):
    socket.send(np.array(data).astype(np.float32).tobytes())