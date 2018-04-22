# -*- coding: utf-8 -*-
# @Author: TheoLong
# @Date:   2018-04-15 00:38:15
# @Last Modified by:   TheoLong
# @Last Modified time: 2018-04-22 18:04:16
import RPi.GPIO as GPIO
from led_pins import led_pins
import time
import json
import socket
import pickle
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

target_state = {'red': 100, 'green': 0.1, 'blue': 100, 'rate': 0.05, 'status' = 1}
current_state = {'red': 0.1, 'green': 0.1, 'blue': 0.1}
sleep_rate = target_state['rate']
on_off = target_state['status']

#creating socket
host = ''
port = 8081
backlog = 5
size = 1024
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("======= Created socket on port " + str(port))
except socket.error as message:
    if s:
        s.close()
    print ("======= Unable to open socket: " + str(message))    
s.bind((host, port))
s.listen(backlog)

#================   main    =========================


#initial start
R = GPIO.PWM(led_pins['red'], current_state['red']) 
G = GPIO.PWM(led_pins['green'], current_state['green'])
B = GPIO.PWM(led_pins['blue'], current_state['blue'])

R.start(0)
G.start(0)
B.start(0)

#change state:
try:
    while 1:
        client, address = s.accept()
        new_state = pickle.loads(client.recv(size))
        if new_state:
            if 'request' in package.key():
                client.send(pickle.dumps(current_state))
            else:
                target_state = new_state
                sleep_rate = target_state['rate']
                on_off = target_state['status']
              
        if on_off == 1:
            red = current_state['red']
            redt = target_state['red']
            green = current_state['green']
            greent = target_state['green']
            blue = current_state['blue']
            bluet = target_state['blue']
            #update ======================      red
            diff = red - redt
            #going up
            if diff < 0:
                if -1 < diff < 0:
                    red = redt
                else:
                    red = red + 1
            #going down
            elif diff > 0:
                if 1 < diff < 0:
                    red = redt
                else:
                    red = red - 1
            #check range
            if red > 100: 
                red = 100;
            elif red <= 0:
                red = 0.1;

            #update ======================      green
            diff = green - greent
            #going up
            if diff < 0:
                if -1 < diff < 0:
                    green = greent
                else:
                    green = green + 1
            #going down
            elif diff > 0:
                if 1 < diff < 0:
                    green = greent
                else:
                    green = green - 1
            #check range
            if green > 100: 
                green = 100;
            elif green <= 0:
                green = 0.1;

                        #update ======================      blue
            diff = blue - bluet
            #going up
            if diff < 0:
                if -1 < diff < 0:
                    blue = bluet
                else:
                    blue = blue + 1
            #going down
            elif diff > 0:
                if 1 < diff < 0:
                    blue = bluet
                else:
                    blue = blue - 1
            #check range
            if blue > 100: 
                blue = 100;
            elif blue <= 0:
                blue = 0.1;

            current_state['red'] = red
            current_state['green'] = green
            current_state['blue'] = blue
            
            R.ChangeDutyCycle(red)
            R.ChangeDutyCycle(green)
            R.ChangeDutyCycle(blue)
            

            #sleep to rate
            print (current_state)
            time.sleep(sleep_rate)
        else:
            R.ChangeDutyCycle(0.1)
            R.ChangeDutyCycle(0.1)
            R.ChangeDutyCycle(0.1)
            current_state['red'] = 0.1
            current_state['green'] = 0.1
            current_state['blue'] = 0.1

except KeyboardInterrupt:
    pass
R.stop()
G.stop()
B.stop()
GPIO.cleanup()




