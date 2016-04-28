#!/usr/bin/python
import sys, struct, array, time, io, os, fcntl, datetime
import RPi.GPIO as GPIO

I2C_SLAVE=0x0703
HTU21D_ADDR = 0x40
CMD_READ_TEMP_HOLD = "\xE3"
CMD_READ_HUM_HOLD = "\xE5"
CMD_READ_TEMP_NOHOLD = "\xF3"
CMD_READ_HUM_NOHOLD = "\xF5"
CMD_WRITE_USER_REG = "\xE6"
CMD_READ_USER_REG = "\xE7"
CMD_SOFT_RESET= "\xFE"

ac_state = 0

# Set up LED and AC relay
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
GPIO.setup(7, GPIO.OUT) ## Setup GPIO Pin 7 to OUT
GPIO.setup(11, GPIO.OUT) ## Setup GPIO Pin 7 to OUT

class i2c(object):
   def __init__(self, device, bus):

      self.fr = io.open("/dev/i2c-"+str(bus), "rb", buffering=0)
      self.fw = io.open("/dev/i2c-"+str(bus), "wb", buffering=0)

      # set device address

      fcntl.ioctl(self.fr, I2C_SLAVE, device)
      fcntl.ioctl(self.fw, I2C_SLAVE, device)

   def write(self, bytes):
      self.fw.write(bytes)

   def read(self, bytes):
      return self.fr.read(bytes)

   def close(self):
      self.fw.close()
      self.fr.close()

class HTU21D(object):
   def __init__(self):
      self.dev = i2c(HTU21D_ADDR, 1) #HTU21D 0x40, bus 1
      self.dev.write(CMD_SOFT_RESET) #soft reset
      time.sleep(.1)

   def ctemp(self, sensorTemp):
      tSensorTemp = sensorTemp / 65536.0
      return -46.85 + (175.72 * tSensorTemp)

   def chumid(self, sensorHumid):
      tSensorHumid = sensorHumid / 65536.0
      return -6.0 + (125.0 * tSensorHumid)

   def crc8check(self, value):
      # Ported from Sparkfun Arduino HTU21D Library: https://github.com/sparkfun/HTU21D_Breakout
      remainder = ( ( value[0] << 8 ) + value[1] ) << 8
      remainder |= value[2]
      
      # POLYNOMIAL = 0x0131 = x^8 + x^5 + x^4 + 1
      # divsor = 0x988000 is the 0x0131 polynomial shifted to farthest left of three bytes
      divsor = 0x988000
      
      for i in range(0, 16):
         if( remainder & 1 << (23 - i) ):
            remainder ^= divsor
         divsor = divsor >> 1
      
      if remainder == 0:
         return True
      else:
         return False
   
   def read_tmperature(self):
      self.dev.write(CMD_READ_TEMP_NOHOLD) #measure temp
      time.sleep(.1)

      data = self.dev.read(3)
      buf = array.array('B', data)

      if self.crc8check(buf):
         temp = (buf[0] << 8 | buf [1]) & 0xFFFC
         return self.ctemp(temp)
      else:
         return -255
         
   def read_humidity(self):
      self.dev.write(CMD_READ_HUM_NOHOLD) #measure humidity
      time.sleep(.1)

      data = self.dev.read(3)
      buf = array.array('B', data)
      
      if self.crc8check(buf):
         humid = (buf[0] << 8 | buf [1]) & 0xFFFC
         return self.chumid(humid)
      else:
         return -255

if __name__ == "__main__":
   # Open logging file
#   if len(sys.argv) != 2:
#      print 'Usage: python ', sys.argv[0], '<logfile.csv>'
#   filename = '/tmp/' + sys.argv[1]
#   try:
#      file = open(filename, 'a')
#   except IOError:
#      print "Could not open:", filename
#      exit(1)
#   print "Opened in append mode:", filename

   # Create humdity sensor object
   obj = HTU21D()
   base_date = datetime.datetime(1970,1,1)
   now = datetime.datetime.now()
#   target = int((now-base_date).total_seconds())
   # Round up to next 5 minute boundary
#   target = ((target + 299) / 300) * 300
   while True:
      GPIO.output(7,True) ## Turn on GPIO pin 7
      # Get current datetime
      now = datetime.datetime.now()
#      print target
#      now_seconds = int((now-base_date).total_seconds())
#      print now_seconds
#      if now_seconds >= target:
      # Read temp and humidity and log to file
      temp = obj.read_tmperature()
      tempf = (temp * 1.8) + 32
      humid = obj.read_humidity()
      print tempf

      if (tempf>74):
	if (ac_state == 0):
	  GPIO.output(11,True) 
	  ac_state = 1
	  print "Air conditioner ON"
      else:
	if (ac_state == 1):
  	  GPIO.output(11,False)
	  ac_state = 0
	  print "Air conditioner OFF"

#      out_string = "%d-%02d-%02d %02d:%02d,%.1f,%.1f" % (now.year, now.month, now.day, now.hour, now.minute, temp, humid)
#      print out_string
#         print >>file, out_string
#         file.flush()
#         os.fsync(file)
#         target += 300 # Advance target by 5 minutes

      GPIO.output(7,False) ## Turn on GPIO pin 7
      time.sleep(30)
