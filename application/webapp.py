from flask import Flask
import dht11
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
instance = dht11.DHT11(pin=14)

app = Flask(__name__)

# Lib is unstable, retry couple of times, if fail occurs
# TODO: find another sensor lib
def fetch_sensor_data(times = 5):
    result = instance.read()
    if not result.is_valid() and times > 0:
        times -= 1
        time.sleep(1)
        return fetch_sensor_data(times)
    return result


@app.route("/metrics")
def metrics():
    dht11_data = ""
    result = fetch_sensor_data()
    if result.is_valid():
        dht11_data = f"""pihome_temperature {result.temperature}
pihome_humidity {result.humidity}"""

    return f"{dht11_data}", 200, {'Content-Type': 'text/plain; charset=utf-8'}

if __name__ == "__main__":
    app.run(host='0.0.0.0')
