import RPi.GPIO as GPIO
import settings

class Heater():
    def __init__(self):
        self.powerlevel = 0
        self.r1 = settings.R1
        self.r2 = settings.R2
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.r1, GPIO.OUT)
        GPIO.setup(self.r2, GPIO.OUT)
        GPIO.output(self.r1, 0)
        GPIO.output(self.r2, 0)

    def set_power(self, powerlevel):
        self.powerlevel = powerlevel
        if self.powerlevel == 1:
            GPIO.output(self.r1, 1)
            GPIO.output(self.r2, 0)
        elif self.powerlevel == 2: 
            GPIO.output(self.r1, 0)
            GPIO.output(self.r2, 1)
        elif self.powerlevel == 3: 
            GPIO.output(self.r1, 1)
            GPIO.output(self.r2, 1)
        else:
            self.stop()

    def stop(self):
        GPIO.output(self.r1, 0)
        GPIO.output(self.r2, 0)