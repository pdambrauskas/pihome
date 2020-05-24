import threading
import bluetooth
from providers.support.models import Metric

class Bluetooth:
    def __init__(self, duration=20):
        self.duration = duration
        self.nearby_devices = []
        self.thread = threading.Thread(target=self._track)

    def run(self):
       self.thread.start()

    def read(self):
        return [Metric("pihome_bluetooth_device", 1, {'device': name}) for _addr, name in self.nearby_devices]

    def _track(self):
        while True:
            self.nearby_devices = bluetooth.discover_devices(duration=self.duration, lookup_names=True)
