from providers.support import dht11
import time
from providers.support.models import Metric

class TemperatureSensor:
    def __init__(self, data_pin):
        self.sensor = dht11.DHT11(pin=data_pin)

    def read(self, retries=5):
        result = self.sensor.read()
        if not result.is_valid() and retries > 0:
            retries -= 1
            time.sleep(1)
            try:
                return self.read(retries)
            except:
                return []
        if result.is_valid:
            return [
                Metric("pihome_temperature", result.temperature),
                Metric("pihome_humidity", result.humidity)
            ]

        return []
