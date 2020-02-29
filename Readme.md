# Monitoring Apartment temperature & humidity with Raspberry Pi, Prometheus & Grafana

For quite some time, I had a spare Raspberry Pi lying around in my place. And one weekend I came up with idea to make my apartment "smarter". What I mean by saying "smarter" is tracking some metrics of my surroundings.

I have some experience in working with [Prometheus](https://prometheus.io/) and [Grafana](https://grafana.com/), so I decided to incorporate those tools into my solution. Yes, it does sound like overengineering simple task, you can probably get same results in much simpler way : ).

In this post I'll describe my setup for monitoring room temperature & humidity.

## Hardware components

These are all the component, I used in my project:
- [Raspberry Pi 3 Model B](https://www.raspberrypi.org/products/raspberry-pi-3-model-b/)
- 16 GB microSD card
- [DHT11 Temperature And Humidity Sensor](https://components101.com/dht11-temperature-sensor)
- Mobile phone charger, for powering Raspberry Pi

## Connecting Sensor to Raspberry Pi

I connected Ground pin to the Ground of Raspberry PI, Data Pin to GPIO 14 pin, Vcc pin to 3.3V power supply pin.

## Reading sensor data

For reading sensor data and feeding it to Prometheus, I chose [DHT11_Python](https://github.com/szazo/DHT11_Python) library, which is quite unstable, and sometimes does not return valid results, so you might get some gaps in your graphs.

Also I've created simple Flask API to serve metrics for Prometheus:
```python
from flask import Flask
import dht11
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
instance = dht11.DHT11(pin=14)

app = Flask(__name__)

@app.route("/metrics")
def metrics():
    dht11_data = ""
    result = instance.read()
    if result.is_valid():
        dht11_data = f"""pihome_temperature {result.temperature}
pihome_humidity {result.humidity}"""

    return f"{dht11_data}", 200, {'Content-Type': 'text/plain; charset=utf-8'}

if __name__ == "__main__":
    app.run(host='0.0.0.0')
```

## Prometheus configuration

To scrape metrics from my Flask API, I've added configuration to `prometheus.yml`:

```yaml
global:
    scrape_interval: 30s
scrape_configs:
    - job_name: 'pihome'
      static_configs:
        - targets: [pihome:5000]
```

## Grafana Configuration

Then, in `/etc/grafana/provisioning`, I've added datasource configuration:
```yaml
apiVersion: 1
datasources:
  - name: Prometheus
    type: prometheus
    url: http://prometheus:9090/
    access: proxy
    isDefault: true
```
It is also possible to add Grafana dashboards to provisioning folder as json files, so that you don't need to create new dashboard each time you re-deploy Grafana.

## Connecting everything together

To make everything portable and easy to install, I packed my Flask API to Docker image and configured all services in `docker-compose.yaml`:
```yaml

version: '3'

services:
  pihome:
    image: pihome
    build: .
    restart: always
    devices:
      - "/dev/mem:/dev/mem"
    privileged: true
    ports:
      - 5000:5000
 
  prometheus:
    image: prom/prometheus:v2.16.0
    user: root
    volumes:
      - ./prometheus/:/etc/prometheus/
      - /var/prometheus:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--storage.tsdb.retention.time=30d'
      - '--web.console.libraries=/usr/share/prometheus/console_libraries'
      - '--web.console.templates=/usr/share/prometheus/consoles'
    ports:
      - 9090:9090
    depends_on:
      - pihome
    restart: always

  grafana:
    image: grafana/grafana:6.6.2
    depends_on:
      - prometheus
    ports:
      - 80:3000
    volumes:
      - ./grafana/:/etc/grafana
    restart: always
```

## Git project

You can find my full configuration and code on Github: https://github.com/pdambrauskas/pihome 

