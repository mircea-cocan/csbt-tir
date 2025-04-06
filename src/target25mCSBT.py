import time
import RPi.GPIO as GPIO

class Target():
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)

    def start(self):
        pass

    def off(self):
        self.switch()

    def on(self):
        self.switch()

    def switch(self):
        GPIO.output(self.pin, True)
        time.sleep(.3)
        GPIO.output(self.pin, False)



