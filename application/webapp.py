from flask import Flask
from providers.temperature import TemperatureSensor
from providers.motion import Motion
from providers.bluetooth import Bluetooth
from providers.wifi import Wifi
import RPi.GPIO as GPIO
import time
import os

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

temperature = TemperatureSensor(14)

motion = Motion(17)
motion.run()

bluetooth = Bluetooth()
bluetooth.run()

wifi = Wifi(os.environ['NETWORK_TO_SCAN'])
wifi.run()

app = Flask(__name__)

@app.route("/metrics")
def metrics():
    metrics = temperature.read() + motion.read() + bluetooth.read() + wifi.read()
    result = [metric.to_prometheus() for metric in metrics]
    return "\n".join(result), 200, {'Content-Type': 'text/plain; charset=utf-8'}

if __name__ == "__main__":
    app.run(host='0.0.0.0')
