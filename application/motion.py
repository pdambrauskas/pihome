import RPi.GPIO as GPIO
import time
import threading

class Motion:
    def __init__(self, pin):
        self.pin = pin
        self.motions = 0
        GPIO.setup(pin, GPIO.IN)
        self.thread = threading.Thread(target=self._track)
    
    def run(self):
       self.thread.start()
    
    def read(self):
        return self.motions

    def _track(self):
        while True:
            if GPIO.input(self.pin):
                self.motions += 1
                # Reset to avoid overflow
                if self.motions > 900:
                    self.motions = 0
            time.sleep(1)
