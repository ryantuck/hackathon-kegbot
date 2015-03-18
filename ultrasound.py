
# ultrasound code

import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BCM)

class Ultrasound():

    def __init__(self):

        # define pins
        self.trig = 23
        self.echo = 24

    def iterate(self):

        gpio.setup(self.trig,gpio.OUT)
        gpio.setup(self.echo.gpio.IN)

        gpio.output(self.trig,False)

        print 'waiting for sensor to settle'

        time.sleep(2)

        gpio.output(self.trig,True)

        time.sleep(0.0001)

        gpio.output(self.trig,False)

        while gpio.input(self.echo) == 0:
            pulse_start = time.time()

        while gpio.input(self.echo) == 1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start

        distance = pulse_duration * 17150
        distance = round(distance,2)

        print 'distance: ', distance, 'cm'

gpio.cleanup()


