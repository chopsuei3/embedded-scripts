#!/usr/bin/python
import os
import threading
import rrdtool
from Subfact_ina219 import INA219

os.chdir("/home/pi")

currentrrd = "/home/pi/current.rrd"
shuntrrd = "/home/pi/shunt.rrd"
busrrd = "/home/pi/bus.rrd"

if not os.path.exists(currentrrd):
  print 'Creating RRDtool database at ' + 'currentrrd'
  try:
    rrdtool.create(currentrrd,
    "--step","1",
    'DS:current:GAUGE:5:U:U',
    'RRA:LAST:0.5:1:3600',
    'RRA:AVERAGE:0.5:10:864'
    )
  except rrdtool.error, e:
    print e
    raise Exception, 'Unable to create instant RRDtool database!'
else:
  print 'Using RRDtool database at ' + 'currentrrd'

if not os.path.exists(shuntrrd):
  print 'Creating RRDtool database at ' + 'shuntrrd'
  try:
    rrdtool.create(shuntrrd,
    "--step","1",
    'DS:shunt:GAUGE:5:U:U',
    'RRA:LAST:0.5:1:3600',
    'RRA:AVERAGE:0.5:10:864'
    )
  except rrdtool.error, e:
    print e
    raise Exception, 'Unable to create instant RRDtool database!'
else:
  print 'Using RRDtool database at ' + 'shuntrrd'

if not os.path.exists(busrrd):
  print 'Creating RRDtool database at ' + 'busrrd'
  try:
    rrdtool.create(busrrd,
    "--step","1",
    'DS:bus:GAUGE:5:U:U',
    'RRA:LAST:0.5:1:3600',
    'RRA:AVERAGE:0.5:10:864'
    )
  except rrdtool.error, e:
    print e
    raise Exception, 'Unable to create instant RRDtool database!'
else:
  print 'Using RRDtool database at ' + 'busrrd'

ina = INA219()

def update_graph():
   threading.Timer(5.0,update_graph).start()
   print "Updating current graph"
   rrdtool.graph("/var/www/html/current.png",
   "-s end-60m",
   "-w 720",
   "-t Current (mA)",
   "-v Current (mA)",
   "-X 0",
   "DEF:current=current.rrd:current:LAST",
   "LINE1:current#0000FF:Current",
#   "VDEF:totalflow10actual=flow,TOTAL",
   "GPRINT:current:LAST:%4.2lf"
   )	

   print "Updating bus graph"
   rrdtool.graph("/var/www/html/bus.png",
   "-s end-60m",
   "-w 720",
   "-t Bus (V)",
   "-v Bus (V)",
   "-X 0",
   "DEF:bus=bus.rrd:bus:LAST",
   "LINE1:bus#0000FF:bus",
#   "VDEF:totalflow10actual=flow,TOTAL",
   "GPRINT:bus:LAST:%4.2lf"
   )	

   print "Updating shunt graph"
   rrdtool.graph("/var/www/html/shunt.png",
   "-s end-60m",
   "-w 720",
   "-t Shunt (mV)",
   "-v Shunt (mV)",
   "-X 0",
   "DEF:shunt=shunt.rrd:shunt:LAST",
   "LINE1:shunt#0000FF:shunt",
#   "VDEF:totalflow10actual=flow,TOTAL",
   "GPRINT:shunt:LAST:%4.2lf"
   )	

def get_reading():
   threading.Timer(1.0,get_reading).start()
   result = ina.getBusVoltage_V()
   bus = ina.getBusVoltage_V()
   shunt = ina.getShuntVoltage_mV()
   current = ina.getCurrent_mA()
   rrdtool.update(currentrrd,'N:' + `current`)
   print rrdtool.error()
   rrdtool.update(busrrd,'N:' + `bus`)
   print rrdtool.error()
   rrdtool.update(shuntrrd,'N:' + `shunt`)
   print rrdtool.error()
#   print "Shunt   : %.3f mV" % ina.getShuntVoltage_mV()
#   print "Bus     : %.3f V" % ina.getBusVoltage_V()
#   print "Current : %.3f mA" % ina.getCurrent_mA()
   print current
   print bus
   print shunt

get_reading()
update_graph()
