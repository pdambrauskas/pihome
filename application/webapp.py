from flask import Flask
from temperature import TemperatureSensor
from motion import Motion
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

temperature = TemperatureSensor(14)
motion = Motion(17)
motion.run()

app = Flask(__name__)

@app.route("/metrics")
def metrics():
    temperature_data = ""
    result = temperature.read()
    if result.is_valid():
        temperature_data = f"""pihome_temperature {result.temperature}
pihome_humidity {result.humidity}"""

    return f"""{temperature_data}
pihome_movement {motion.read()}""", 200, {'Content-Type': 'text/plain; charset=utf-8'}

if __name__ == "__main__":
    app.run(host='0.0.0.0')
