
from flask import Flask, render_template, jsonify
from ultrasound import *
from flowmeter import *
import RPi.GPIO as GPIO

ultrasound = Ultrasound()
app = Flask(__name__)

total_poured_left = 0
total_poured_right = 0
beer_count = 0


def ultrasoundStuff():
    return ultrasound.checkForHuman()


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
    currentTime = int(time.time() * FlowMeter.MS_IN_A_SECOND)
    global beer_count
    left_pour = 0
    right_pour = 0
    left_beer = left_meter.beverage
    right_beer = right_meter.beverage
    #5 sec pause
    if left_meter.thisPour > 0.23 and currentTime - left_meter.lastClick > 5000:
        left_pour = left_meter.getFormattedThisPour()
        left_meter.thisPour = 0.0
        beer_count = beer_count + 1

    if right_meter.thisPour > 0.23 and currentTime - right_meter.lastClick > 5000:
        right_pour = right_meter.getFormattedThisPour()
        right_meter.thisPour = 0.0
        beer_count = beer_count + 1
    
    global total_poured_left
    global total_poured_right
    total_poured_left = int(left_pour) + int(total_poured_left)
    total_poured_right = int(right_pour) + int(total_poured_right)

    return {left_beer: left_pour, right_beer: right_pour}



#set up gpio
GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27,GPIO.IN, pull_up_down=GPIO.PUD_UP)

left_meter = FlowMeter('metric', 'Allagash Black') #gpio 17
right_meter = FlowMeter('metric', 'Bengali Tiger') #gpio 27

GPIO.add_event_detect(17, GPIO.RISING, callback=tick_left_meter, bouncetime=20) # left tap
GPIO.add_event_detect(27, GPIO.RISING, callback=tick_right_meter, bouncetime=20) # right tap

def getBestBeer():
    if total_poured_left > total_poured_right:
        return left_meter.beverage
    else:
        return right_meter.beverage

def getWorstBeer():
    if total_poured_left > total_poured_right:
        return right_meter.beverage
    else:
        return left_meter.beverage


@app.route("/")
def measure():

    templateData = {
        'last_pour' : flow_stuff(),
        'ultrasound' : ultrasoundStuff(),
        'beer_count': beer_count,
        'best_beer': getBestBeer(),
        'worst_beer': getWorstBeer(),
    }

    return render_template('index.html', **templateData)

@app.route("/metrics.json")
def metrics_json():
    return jsonify({
        'last_pour': flow_stuff(),
        'ultrasound': ultrasoundStuff(),
        'best_beer': getBestBeer(),
        'beer_count': beer_count,
        'worst_beer': getWorstBeer(),
    })

if __name__ == '__main__':
        app.run(host='0.0.0.0', port=80, debug=True)


