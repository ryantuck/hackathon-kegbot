
from flask import Flask
import threading
from ultrasound import *
from flowmeter import *
import RPi.GPIO as GPIO

ultrasound = Ultrasound()
app = Flask(__name__)

@app.route('/')
def hello():
    return 'hello world!'


def flaskStuff():
    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=80, debug=True)


def ultrasoundStuff():
    while True:
        ultrasound.iterate()


def tick_left_meter(channel):
    print left_meter.beverage
    currentTime = int(time.time() * FlowMeter.MS_IN_A_SECOND)
    if left_meter.enabled == True:
        left_meter.update(currentTime)


def tick_right_meter(channel):
    print right_meter.beverage
    currentTime = int(time.time() * FlowMeter.MS_IN_A_SECOND)
    if right_meter.enabled == True:
        right_meter.update(currentTime)

def flow_stuff():
    while True:
        currentTime = int(time.time() * FlowMeter.MS_IN_A_SECOND)

        #5 sec pause
        if left_meter.thisPour > 0.23 and currentTime - left_meter.lastClick > 5000:
            print left_meter.getFormattedThisPour()

        if right_meter.thisPour > 0.23 and currentTime - right_meter.lastClick > 5000:
            print right_meter.getFormattedThisPour()




# set up threading
threads = []
flaskThread = threading.Thread(target=flaskStuff)
flowThread = threading.Thread(target=flow_stuff)
ultrasoundThread = threading.Thread(target=ultrasoundStuff)

flaskThread.daemon = True
flowThread.daemon = True
ultrasoundThread = True

threads.append(flaskThread)
threads.append(flowThread)
threads.append(ultrasoundThread)

left_meter = FlowMeter('metric', 'Allagash Black') #gpio 17
right_meter = FlowMeter('metric', 'Bengali Tiger') #gpio 27

GPIO.add_event_detect(17, GPIO.RISING, callback=tick_left_meter, bouncetime=20) # left tap
GPIO.add_event_detect(27, GPIO.RISING, callback=tick_right_meter, bouncetime=20) # right tap

flaskThread.start()
flowThread.start()
ultrasoundThread.start()

import time
while True:
    time.sleep(1)


