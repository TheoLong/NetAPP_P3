# -*- coding: utf-8 -*-
# @Author: TheoLong
# @Date:   2018-04-15 00:38:15
# @Last Modified by:   TheoLong
# @Last Modified time: 2018-04-22 13:33:50
import RPi.GPIO as GPIO
import led_pins
from flask import Flask, request, Response, make_response
'''
==================  initialize  ====================
'''

if led_pins[3] == 'BOARD':
    GPIO.setmode(GPIO.BOARD)
elif led_pins[3] == "BCM":
    GPIO.setmode(GPIO.BCM)
else:
    exit('Error: invalid GPIO mode')

chan_list = [led_pins[0],led_pins[1],led_pins[2]]  # in the order of RGB
GPIO.setup(chan_list, GPIO.OUT) # set to output

target_state = {'red': 100, 'green': 0, 'blue': 100}
current_state = {'red': 0, 'green': 0, 'blue': 0}
sleep_rate = 0.05
on_off = 1

'''
==================  change color  ====================
'''
@app.route('/led', strict_slashes=True, methods=['POST'])
def changeState():
    new_state = request.get_json()
    if 'red' in new_state.key():
        if 0<= new_state['red'] <= 100:
            target_state['red'] = new_state['red']

    if 'green' in new_state.key():
        if 0<= new_state['green'] <= 100:
            target_state['green'] = new_state['green']

    if 'blue' in new_state.key():
        if 0<= new_state['blue'] <= 100:
            target_state['blue'] = new_state['blue']

    if 'rate' in new_state.key():
        sleep_rate = new_state['rate']

    if 'state' in new_state.key():
        on_off = state


@app.route('/t1', strict_slashes=True, methods=['GET'])
def get_t1():
    report = current_state
    report['rate'] = sleep_rate
    report['state'] = on_off
    return report


#================   main    =========================
app.run(host='0.0.0.0', port=8081, debug=True)

#initial start
R = GPIO.PWM(led_pins[0], current_state['red']) 
G = GPIO.PWM(led_pins[1], current_state['green'])
B = GPIO.PWM(led_pins[2], current_state['blue'])

R.start(0)
G.start(0)
B.start(0)

#change state:
try:
    while 1:
        if on_off == 1:
            #changing red
            if (current_state['red'] - target_state['red']) < 0:
                current_state['red'] = current_state['red'] + 1
                R.ChangeDutyCycle(current_state['red'])
            elif (current_state['red'] - target_state['red']) > 0:
                current_state['red'] = current_state['red'] - 1
                R.ChangeDutyCycle(current_state['red'])

            #changing green
            if (current_state['green'] - target_state['green']) < 0:
                current_state['green'] = current_state['green'] + 1
                R.ChangeDutyCycle(current_state['green'])
            elif (current_state['green'] - target_state['green']) > 0:
                current_state['green'] = current_state['green'] + -
                R.ChangeDutyCycle(current_state['green'])

            #changing blue
            if (current_state['blue'] - target_state['blue']) < 0:
                current_state['blue'] = current_state['blue'] + 1
                R.ChangeDutyCycle(current_state['blue'])
            elif (current_state['blue'] - target_state['blue']) > 0:
                current_state['blue'] = current_state['blue'] - 1
                R.ChangeDutyCycle(current_state['blue'])

            #sleep to rate
            sleep(sleep_rate)
        else:
            R.ChangeDutyCycle(0)
            R.ChangeDutyCycle(0)
            R.ChangeDutyCycle(0)
            current_state['red'] = 0
            current_state['green'] = 0
            current_state['blue'] = 0

except KeyboardInterrupt:
    pass
p.stop()
GPIO.cleanup()



