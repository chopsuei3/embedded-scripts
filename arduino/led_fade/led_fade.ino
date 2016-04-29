// LED fader test
// Fade up and fade down.
// Repeat.
/*
   Hardware:
   This code was developed using the SparkFun breakout board:
   http://www.sparkfun.com/products/10901
   Connections are:
   VCNL4000 Breakout ---------------- Arduino
        3.3V  -----------------------  3.3V
        GND  ------------------------  GND
        SCL  ------------------------  A5
        SDA  ------------------------  A4
        IR+  ------------------------  5V (3.3V is fine too)
 */

#include <Wire.h>

#define VCNL4000_ADDRESS 0x13  // 0x26 write, 0x27 read

// VCNL4000 Register Map
#define COMMAND_0 0x80  // starts measurments, relays data ready info
#define PRODUCT_ID 0x81  // product ID/revision ID, should read 0x11
#define IR_CURRENT 0x83  // sets IR current in steps of 10mA 0-200mA
#define AMBIENT_PARAMETER 0x84  // Configures ambient light measures
#define AMBIENT_RESULT_MSB 0x85  // high byte of ambient light measure
#define AMBIENT_RESULT_LSB 0x86  // low byte of ambient light measure
#define PROXIMITY_RESULT_MSB 0x87  // High byte of proximity measure
#define PROXIMITY_RESULT_LSB 0x88  // low byte of proximity measure
#define PROXIMITY_FREQ 0x89  // Proximity IR test signal freq, 0-3
#define PROXIMITY_MOD 0x8A  // proximity modulator timing

int ambientValue;
int state = 0;
int fadespeed = 5;
int fadeoffspeed = fadespeed/2;


#define LEDPIN 3 
#define FADECONTROL A2
/*
#define fadespeed 5   // make this higher to slow down
#define FADEOFFSPEED fadespeed/2   // make this higher to slow down
*/

void setup()
{
  pinMode(LEDPIN, OUTPUT);
  pinMode(FADECONTROL, INPUT);
  digitalWrite(LEDPIN,LOW);
  Serial.begin(9600);

  Wire.begin();  // initialize I2C stuff
  
  /* Test that the device is working correctly */
  byte temp = readByte(PRODUCT_ID);
  if (temp != 0x11)  // Product ID Should be 0x11
  {
    Serial.print("Something's wrong. Not reading correct ID: 0x");
    Serial.println(temp, HEX);
  }
  else
//    Serial.println("VNCL4000 Online...");
  
  /* Now some VNCL400 initialization stuff
     Feel free to play with any of these values, but check the datasheet first!*/
  writeByte(AMBIENT_PARAMETER, 0x0F);  // Single conversion mode, 128 averages
  writeByte(IR_CURRENT, 20);  // Set IR current to 200mA
  writeByte(PROXIMITY_FREQ, 2);  // 781.25 kHz
  writeByte(PROXIMITY_MOD, 0x81);  // 129, recommended by Vishay
}
  
void loop()
{
//  int fadevalue = analogRead(FADECONTROL);
//  Serial.println(fadevalue);

  fadespeed = analogRead(FADECONTROL)/10 + 5;
  fadeoffspeed = fadespeed/2;
  Serial.println(fadespeed);
  
  ambientValue = readAmbient();
//  Serial.print(ambientValue, DEC);
  
  if(ambientValue == 0 && state == 1)
  {
    turnOff();
    state = 0;
  }
  
  if(ambientValue != 0 && state == 0)
  {
    turnOn();
    state = 1;
  }

  delay(5);
}

// readAmbient() returns a 16-bit value from the VCNL4000's ambient light data registers
unsigned int readAmbient()
{
  unsigned int data;
  byte temp;
  
  temp = readByte(COMMAND_0);
  writeByte(COMMAND_0, temp | 0x10);  // command the sensor to perform ambient measure
  
  while(!(readByte(COMMAND_0)&0x40)) 
    ;  // wait for the proximity data ready bit to be set
  data = readByte(AMBIENT_RESULT_MSB) << 8;
  data |= readByte(AMBIENT_RESULT_LSB);
  
  return data;
}

// writeByte(address, data) writes a single byte of data to address
void writeByte(byte address, byte data)
{
  Wire.beginTransmission(VCNL4000_ADDRESS);
  Wire.write(address);
  Wire.write(data);
  Wire.endTransmission();
}

// readByte(address) reads a single byte of data from address
byte readByte(byte address)
{
  byte data;
  
  Wire.beginTransmission(VCNL4000_ADDRESS);
  Wire.write(address);
  Wire.endTransmission();
  Wire.requestFrom(VCNL4000_ADDRESS, 1);
  while(!Wire.available())
    ;
  data = Wire.read();

  return data;
}

void turnOn()
{
  int g;

  for (g = 0; g < 256; g++) { 
//  Serial.println(g);
  analogWrite(LEDPIN, g);
  delay(fadespeed);
  }
  digitalWrite(LEDPIN, HIGH);
}

void turnOff()
{
  int g;
    
  for (g = 255; g > 0; g--) { 
//    Serial.println(g);
    analogWrite(LEDPIN, g);
    delay(fadeoffspeed);
  }
  digitalWrite(LEDPIN, LOW);
}
