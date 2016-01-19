import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# set up LED on pin RPi pin 11
#GPIO.setup(11, GPIO.OUT)

# set up relay on RPi pin 15
GPIO.setup(15, GPIO.OUT)

state = GPIO.input(15)

if state == False:
	print "OFF"
else:
	print "ON"
