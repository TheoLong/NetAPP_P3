# -*- coding: utf-8 -*-
# @Author: TheoLong
# @Date:   2018-04-15 00:38:15
# @Last Modified by:   TheoLong
# @Last Modified time: 2018-04-15 00:53:48
import RPi.GPIO as GPIO
import led_pins

'''
==================  indivisual color  ====================
'''
def litRGB(R,G,B,duration):
    #clear previous color
    clearAllColor()
    onList = []
    if (R > 0):
        onList.append(RED)
    if (G > 0):
        onList.append(GREEN)
    if (B > 0):
        onList.append(BLUE)

    if (duration > 0): # unlimited time if duration = 0
        GPIO.output(onList, GPIO.HIGH) 
        time.sleep(duration)
        clearAllColor()
    else:
        GPIO.output(onList, GPIO.HIGH) 

def clearAllColor():
    GPIO.output(chan_list, GPIO.LOW) 
    #reset all color


#================   main    =========================

if led_pins[3] == 'BOARD':
    GPIO.setmode(GPIO.BOARD)
elif led_pins[3] == "BCM":
    GPIO.setmode(GPIO.BCM)
else:
    exit('Error: invalid GPIO mode')

chan_list = [led_pins[0],led_pins[1],led_pins[2]]  # in the order of RGB
GPIO.setup(chan_list, GPIO.OUT) # set to output


'''
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)

p = GPIO.PWM(12, 50)  # channel=12 frequency=50Hz
p.start(0)
try:
    while 1:
        for dc in range(0, 101, 5):
            p.ChangeDutyCycle(dc)
            time.sleep(0.1)
        for dc in range(100, -1, -5):
            p.ChangeDutyCycle(dc)
            time.sleep(0.1)
except KeyboardInterrupt:
    pass
p.stop()
GPIO.cleanup()
'''


