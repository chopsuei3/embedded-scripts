import os
import datetime
import time
import threading
import sys
import logging
import RPi.GPIO as GPIO  # GPIO library

## Definitions and variables
FLOW_PULSE_PIN = 11 	#GPIO for flow pulses
LED_PIN = 13			#GPIO for LED
FLOW_PULSE_LED_PIN = 15
flowPulses = 0
lgr = logging.getLogger('logger name')
lgr.setLevel(logging.DEBUG) # log all escalated at and above DEBUG
# add a file handler
fh = logging.FileHandler('/tmp/flow.csv')
fh.setLevel(logging.DEBUG) # ensure all messages are logged to file

frmt = logging.Formatter('%(asctime)s,%(message)s')
fh.setFormatter(frmt)

lgr.addHandler(fh)

def blink_led():
	global flowPulses
	flowPulses += 1
	GPIO.output(LED_PIN, GPIO.HIGH)
	time.sleep(0.1)
	GPIO.output(LED_PIN, GPIO.LOW)

def print_usage():
	global flowPulses
	threading.Timer(10.0,print_usage).start()
	print flowPulses
	lgr.debug(flowPulses)
	flowPulses = 0

## Pin I/O setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) 		## Use Broadcom pin numbers
GPIO.setup(FLOW_PULSE_PIN, GPIO.IN)  	## Flow pulses pin
GPIO.setup(FLOW_PULSE_LED_PIN, GPIO.IN)  	## Flow pulses pin
GPIO.setup(LED_PIN, GPIO.OUT) 	## LED pin

GPIO.add_event_detect(11, GPIO.FALLING, callback=blink_led)  
GPIO.add_event_detect(15, GPIO.FALLING, callback=blink_led)  

try:	
	print_usage()
except:
	GPIO.cleanup()           # clean up GPIO on normal exit  
	sys.exit()