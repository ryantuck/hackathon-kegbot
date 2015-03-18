
from flask import Flask
import threading
from ultrasound import *

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


# set up threading
flaskThread = threading.Thread(target=flaskStuff)
flowThread = threading.Thread(target=flowStuff)
ultrasoundThread = threading.Thread(target=ultrasoundStuff)

flaskThread.daemon = True
flowThread.daemon = True
ultrasoundThread = True

threads.append(flaskThread)
threads.append(flowThread)
threads.append(ultrasoundThread)

flaskThread.start()
flowThread.start()
ultrasoundThread.start()

import time
while True:
    time.sleep(1)


