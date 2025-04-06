from gpiozero import Servo
from time import sleep

class Target():
    def __init__(self, pin):
        self.servo = None
        #pigpio_factory = PiGPIOFactory()
        self.servo = Servo(pin=pin, initial_value=None) #, pin_factory=pigpio_factory)

    def start(self):
        self.on()

    def off(self):
        if self.servo is not None:
            self.servo.value = 1
            sleep(1)
            self.servo.value = None

    def on(self):
        if self.servo is not None:
            self.servo.value = -1
            sleep(1)
            self.servo.value = None

    def switch(self):
        if self.servo is not None:
            self.servo.value = 1
            sleep(1)
            self.servo.value = None
    