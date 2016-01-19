import RPi.GPIO as GPIO
import time
import logging

logging.basicConfig(filename='/var/log/heaterpi.log',level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logging.info('Started HeaterPi')

GPIO.setwarnings(False)
GPIO.cleanup()

GPIO.setmode(GPIO.BOARD)

GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(15, GPIO.OUT)

state = 0

while True:
    input_state = GPIO.input(13)
    if input_state == False:
        logging.info('Button Pressed')
        time.sleep(0.2)
	if state == False:
		state = 1
		logging.info('State changed to true')
		GPIO.output(11, True)
		GPIO.output(15, True)
	else:
		state = 0
		logging.info('State changed to false')
		GPIO.output(11, False)
		GPIO.output(15, False)
