# -*- coding: utf-8 -*-
# @Author: TheoLong
# @Date:   2018-04-15 00:38:15
# @Last Modified by:   TheoLong
# @Last Modified time: 2018-04-23 17:09:38
import RPi.GPIO as GPIO
from led_pins import led_pins
import time
import json
import socket
from flask import Flask, request, Response, make_response
from multiprocessing import Process, Value, Array, Manager
from zeroconf import ServiceInfo, Zeroconf

'''
==================  zeroconf  ====================
'''
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('www.google.com', 0))
ipAddress = s.getsockname()[0]
desc = {'path': '/~paulsm/'}
info = ServiceInfo("_http._tcp.local.",
                       "LED._http._tcp.local.",
                       socket.inet_aton(ipAddress), 8081, 0, 0,
                       desc, "ash-2.local.")

zeroconf = Zeroconf()
print("Registration of a service " +str(ipAddress))
zeroconf.register_service(info)
'''
==================  initialize  ====================
'''
if led_pins['mode'] == 10:
    GPIO.setmode(GPIO.BOARD)
elif led_pins['mode'] == 11:
    GPIO.setmode(GPIO.BCM)
else:
    exit('Error: invalid GPIO mode')

chan_list = [led_pins['red'],led_pins['green'],led_pins['blue']]  # in the order of RGB
GPIO.setup(chan_list, GPIO.OUT) # set to output
R = GPIO.PWM(led_pins['red'], 50) 
G = GPIO.PWM(led_pins['green'], 50)
B = GPIO.PWM(led_pins['blue'], 50)

R.start(0)
B.start(0)
G.start(0)

target_state = {'red': 0, 'green': 0, 'blue': 0, 'rate': 0.01, 'status': 1}
current_state = {'red': 0, 'green': 0, 'blue': 0, 'rate': 0.01, 'status': 1}

#================   functions    =========================
app = Flask(__name__)
@app.route('/led', strict_slashes=True, methods=['POST'])
def changeState():
    global target_state
    global sleep_rate 
    global on_off
    new_state = json.loads(request.get_data().decode('utf-8'))
    for key in new_state.keys():
        if key in target_state.keys():
            target_state[key] = new_state[key]
    sleep_rate = target_state['rate']
    on_off = target_state['state']
    print (target_state)
    updateLED()
    return "LED update completed"


@app.route('/led', strict_slashes=True, methods=['GET'])
def report():
    global current_state
    report = current_state
    report['rate'] = sleep_rate
    report['state'] = on_off
    report = json.dumps(report)
    return report

#================   main    =========================

def updateLED():
    #initial start
    global target_state
    global current_state

    #change state:

    notDone = 3
    # try:
    while 1:
        if current_state['state'] == 1:
            red = current_state['red']
            redt = target_state['red']
            green = current_state['green']
            greent = target_state['green']
            blue = current_state['blue']
            bluet = target_state['blue']


            #update ======================      red
            rdiff = red - redt
            #going up
            if rdiff < 0:
                if -1 < rdiff < 0:
                    red = redt
                else:
                    red = red + 1
            #going down
            elif rdiff > 0:
                if 1 < rdiff < 0:
                    red = redt
                else:
                    red = red - 1
            #check range
            if red > 100: 
                red = 100;
            elif red <= 0:
                red = 0;

            #update ======================      green
            gdiff = green - greent
            #going up
            if gdiff < 0:
                if -1 < gdiff < 0:
                    green = greent
                else:
                    green = green + 1
            #going down
            elif gdiff > 0:
                if 1 < gdiff < 0:
                    green = greent
                    greenDone = 1
                else:
                    green = green - 1
            #check range
            if green > 100: 
                green = 100;
            elif green <= 0:
                green = 0;

            #update ======================      blue
            bdiff = blue - bluet
            #going up
            if bdiff < 0:
                if -1 < bdiff < 0:
                    blue = bluet
                else:
                    blue = blue + 1
            #going down
            elif bdiff > 0:
                if 1 < bdiff < 0:
                    blue = bluet
                    blueDone = 1
                else:
                    blue = blue - 1
            #check range
            if blue > 100: 
                blue = 100;
            elif blue <= 0:
                blue = 0;

            current_state['red'] = red
            current_state['green'] = green
            current_state['blue'] = blue

            R.ChangeDutyCycle(red)
            G.ChangeDutyCycle(green)
            B.ChangeDutyCycle(blue)
            

            #sleep to rate
            print (current_state)
            time.sleep(current_state['rate'])
            if rdiff ==0 and gdiff ==0 and bdiff ==0:
                break
        else:

            current_state['red'] = 0
            current_state['green'] = 0
            current_state['blue'] = 0
            R.ChangeDutyCycle(0)
            G.ChangeDutyCycle(0)
            B.ChangeDutyCycle(0)
            break
app.run(host='0.0.0.0', port=8081, debug=True)

GPIO.cleanup()
print("Unregistering...")
zeroconf.unregister_service(info)
zeroconf.close()



