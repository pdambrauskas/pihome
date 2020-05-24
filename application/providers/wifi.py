import threading
import nmap
import time
from providers.support.models import Metric

class Wifi:
    def __init__(self, hosts='192.168.1.0/24'):
        self.hosts = hosts
        self.scan_results = {}
        self.thread = threading.Thread(target=self._track)

    def run(self):
       self.thread.start()

    def read(self):
        metrics = []
        for ip, data in self.scan_results.items():
            mac = data['addresses'].get('mac', 'unknown')
            value = int(data['status']['state'] == 'up')
            labels = {
                'mac': mac,
                'vendor': data['vendor'].get(mac, 'unknown') if mac else 'unknown',
                'hostname': data['hostnames'][0]['name']
            }
            metrics.append(Metric('pihome_network_device', value, labels))

        return metrics

    def _track(self):
        nm = nmap.PortScanner()
        while True:
            rs = nm.scan(hosts=self.hosts, arguments='-sn')
            self.scan_results = rs['scan']
            time.sleep(20)
