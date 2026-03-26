from collections import deque

class LivePlot:
     def __init__(self):
        self.data = deque(maxlen=50)

     def update(self, value):
        self.data.append(value)

     def get_latest(self):
        return list(self.data)[-1] if self.data else 0