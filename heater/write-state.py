import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(11, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)

state = GPIO.input(15)

if state == False:
		GPIO.output(11, True)
		GPIO.output(15, True)
else:
		GPIO.output(11, False)
		GPIO.output(15, False)

