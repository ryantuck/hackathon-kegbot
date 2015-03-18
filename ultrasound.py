
# ultrasound code

import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BCM)

trig = 23
echo = 24

print 'distance measuring in progress'

while True:

    gpio.setup(trig, gpio.OUT)
    gpio.setup(echo, gpio.IN)

    gpio.output(trig,False)

    print 'waiting for sensor to settle'

    time.sleep(2)

    gpio.output(trig,True)

    time.sleep(0.0001)

    gpio.output(trig,False)

    while gpio.input(echo) == 0:
        pulse_start = time.time()

    while gpio.input(echo) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 17150
    distance = round(distance,2)

    print 'distance: ', distance, 'cm'

    GPIO.cleanup()


