import os
import datetime
import time
import threading
import sys
import logging
import rrdtool
import RPi.GPIO as GPIO  # GPIO library

## Definitions and variables
FLOW_PULSE_PIN = 11 	#GPIO for flow pulses
LED_PIN = 13			#GPIO for LED
FLOW_LED_PULSE_PIN = 15

flowPulses = 0

rrdfile = "/home/pi/flow.rrd"
os.chdir("/home/pi")


lgr = logging.getLogger('logger name')
lgr.setLevel(logging.DEBUG) # log all escalated at and above DEBUG
# add a file handler
fh = logging.FileHandler('/tmp/flow.csv')
fh.setLevel(logging.DEBUG) # ensure all messages are logged to file

frmt = logging.Formatter('%(asctime)s')
fh.setFormatter(frmt)

lgr.addHandler(fh)

def blink_led(self):
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
	rrdtool.update(rrdfile,'N:' + `flowPulses`)
	print rrdtool.error()
	update_graph()
	flowPulses = 0

def update_graph():
## Update 10 min actual graph
	print "Updating graph 1"
	rrdtool.graph("/var/www/flow-minutely-actual.png",
	"-s end-10m",
	"-w 720",
	"-t Pulses per second (actual) - Last 10 min",
	"-v Pulses per second",
	"-X 0",
	"DEF:flow=flow.rrd:flow:LAST",
	"LINE1:flow#0000FF:Pulses per second",
	"VDEF:totalflow10actual=flow,TOTAL",
	"GPRINT:totalflow10actual:Total pulses = %4.2lf"
	)	

## Update 10 min average graph
	print "Updating graph 2"
	rrdtool.graph("/var/www/flow-minutely-average.png",
	"-s end-10m",
	"-w 720",
	"-t Pulses per second (minute average) - Last 10 min",
	"-v Pulses per second",
#	"-X 0",
	"DEF:flowMinute=flow.rrd:flow:AVERAGE",
	"LINE1:flowMinute#FF0000:Pulses per second",
	"VDEF:totalflow10average=flowMinute,TOTAL",
	"GPRINT:totalflow10average:Total pulses = %4.2lf"
	)	

## Update hourly actual graph
	print "Updating graph 3"
	rrdtool.graph("/var/www/flow-hourly-actual.png",
	"-s end-1h",
	"-w 720",
	"-t Pulses per second (actual) - Last hour",
	"-v Pulses per second",
	"-X 0",
	"DEF:flow=flow.rrd:flow:LAST",
	"LINE1:flow#0000FF:Pulses per second",
	"VDEF:totalflowhouractual=flow,TOTAL",
	"GPRINT:totalflowhouractual:Total pulses = %4.2lf"
	)	

## Update hourly average graph
	print "Updating graph 4"
	rrdtool.graph("/var/www/flow-hourly-average.png",
	"-s end-1h",
	"-w 720",
	"-t Pulses per second (minute average) - Last hour",
	"-v Pulses per second",
#	"-X 0",
	"DEF:flowMinute=flow.rrd:flow:AVERAGE",
	"LINE1:flowMinute#FF0000:Pulses per second",
	"VDEF:totalflowhouraverage=flowMinute,TOTAL",
	"GPRINT:totalflowhouraverage:Total pulses = %4.2lf"
	)	

## Update daily actual graph
	print "Updating graph 5"
	rrdtool.graph("/var/www/flow-daily-actual.png",
	"-s end-1d",
	"-w 720",
	"-t Pulses per second (actual) - Last day",
	"-v Pulses per second",
	"-X 0",
	"DEF:flow=flow.rrd:flow:LAST",
	"LINE1:flow#0000FF:Pulses per second",
	"VDEF:totalflowdailyactual=flow,TOTAL",
	"GPRINT:totalflowdailyactual:Total pulses = %4.2lf"
	)	

## Update daily average graph
	print "Updating graph 6"
	rrdtool.graph("/var/www/flow-daily-average.png",
	"-s end-1d",
	"-w 720",
	"-t Pulses per second (minute average) - Last day",
	"-v Pulses per second",
#	"-X 0",
	"DEF:flowMinute=flow.rrd:flow:AVERAGE",
	"LINE1:flowMinute#FF0000:Pulses per second",
	"VDEF:totalflowdailyaverage=flowMinute,TOTAL",
	"GPRINT:totalflowdailyaverage:Total pulses = %4.2lf"
	)	

## Update weekly actual graph
	print "Updating graph 7"
	rrdtool.graph("/var/www/flow-weekly-actual.png",
	"-s end-1w",
	"-w 720",
	"-t Pulses per second (actual) - Last week",
	"-v Pulses per second",
	"-X 0",
	"DEF:flow=flow.rrd:flow:LAST",
	"LINE1:flow#0000FF:Pulses per second",
	"VDEF:totalflowweeklyactual=flow,TOTAL",
	"GPRINT:totalflowweeklyactual:Total pulses = %4.2lf"
	)	

## Update weekly average graph
	print "Updating graph 8"
	rrdtool.graph("/var/www/flow-weekly-average.png",
	"-s end-1w",
	"-w 720",
	"-t Pulses per second (minute average) - Last week",
	"-v Pulses per second",
#	"-X 0",
	"DEF:flowMinute=flow.rrd:flow:AVERAGE",
	"LINE1:flowMinute#FF0000:Pulses per second",
	"VDEF:totalflowweeklyaverage=flowMinute,TOTAL",
	"GPRINT:totalflowweeklyaverage:Total pulses = %4.2lf"
	)	


## Pin I/O setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) 		## Use Broadcom pin numbers
GPIO.setup(FLOW_PULSE_PIN, GPIO.IN)  	## Flow pulses pin
GPIO.setup(FLOW_LED_PULSE_PIN, GPIO.IN)  	## Flow pulses pin
GPIO.setup(LED_PIN, GPIO.OUT) 	## LED pin

GPIO.add_event_detect(11, GPIO.FALLING, callback=blink_led)  
#GPIO.add_event_detect(15, GPIO.FALLING, callback=blink_led)  


GPIO.output(LED_PIN, GPIO.HIGH)
time.sleep(2)
GPIO.output(LED_PIN, GPIO.LOW)

if not os.path.exists(rrdfile):
  print 'Creating RRDtool database at ' + 'rrdfile'
  try:
    rrdtool.create(rrdfile,
    "--step","10",
    'DS:flow:ABSOLUTE:20:0:U',
    'RRA:LAST:0.5:1:60480',
    'RRA:AVERAGE:0.5:6:10080'
    )
  except rrdtool.error, e:
    print e
    raise Exception, 'Unable to create instant RRDtool database!'
else:
  print 'Using RRDtool database at ' + 'rrdfile'


try:	
	print_usage()
except:
	GPIO.cleanup()           # clean up GPIO on normal exit  
	sys.exit()
