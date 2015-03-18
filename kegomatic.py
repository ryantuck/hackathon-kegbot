#!/usr/bin/python
import os
import time
import math
import logging
import RPi.GPIO as GPIO
from flowmeter import *

print "Setting up"
#boardRevision = GPIO.RPI_REVISION
GPIO.setmode(GPIO.BCM) # use real GPIO numbering
GPIO.setup(22,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27,GPIO.IN, pull_up_down=GPIO.PUD_UP)

# set up the flow meters
fm = FlowMeter('metric', 'beer')
fm2 = FlowMeter('metric', 'root beer')

# Beer, on Pin 23.
def doAClick(channel):
  print "Do a click 1 called"
  currentTime = int(time.time() * FlowMeter.MS_IN_A_SECOND)
  if fm.enabled == True:
    fm.update(currentTime)

# Root Beer, on Pin 24.
def doAClick2(channel):
  print "Do a click 2 called"
  currentTime = int(time.time() * FlowMeter.MS_IN_A_SECOND)
  if fm2.enabled == True:
    fm2.update(currentTime)

GPIO.add_event_detect(22, GPIO.RISING, callback=doAClick, bouncetime=20) # Beer, on Pin 23
GPIO.add_event_detect(27, GPIO.RISING, callback=doAClick2, bouncetime=20) # Root Beer, on Pin 24

print "Starting Loop"
# main loop
while True:
  
  currentTime = int(time.time() * FlowMeter.MS_IN_A_SECOND)

  if (fm.thisPour > 0.23 and currentTime - fm.lastClick > 10000): # 10 seconds of inactivity causes a tweet
    print fm.getFormattedThisPour()
    fm.thisPour = 0.0
 
  if (fm2.thisPour > 0.23 and currentTime - fm2.lastClick > 10000): # 10 seconds of inactivity causes a tweet
    print fm2.getFormattedThisPour()
    fm2.thisPour = 0.0
