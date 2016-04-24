
#include <SimpleTimer.h>
#include <avr/io.h>
#include <avr/interrupt.h>
#include <SoftwareSerial.h>

const int ledPin =  13;      // the number of the LED pin
const int blinkTime =  50;      // the number of the LED pin

volatile int LEDstate = LOW;

// the timer object
SimpleTimer timer;

int magnetPasses = 0;
int timerId = 0;

void magnetPass() {
  magnetPasses++; // increase by 1

  digitalWrite(ledPin, HIGH);
  delay(blinkTime);
  digitalWrite(ledPin, LOW);
}

void printWaterTotal() {
  Serial.print( "Magnet passes " );
  Serial.println( magnetPasses );
  magnetPasses = 0; // reset counter
}

void setup(void) {
  pinMode(ledPin, OUTPUT);
  Serial.begin(9600);

  attachInterrupt( digitalPinToInterrupt(3), magnetPass, FALLING ); // attach interrupt to external trigger on digital pin 3
  timerId = timer.setInterval( 1000, printWaterTotal ); // call function 'printWaterTotal' every 60 seconds
  
//  Serial.println("Starting capture...");  
}

void loop(){

timer.run();

//Serial.println("Waiting...");
//if(Serial.available())
//{
//  if(Serial.read() == '!')
//  {
//    Serial.println("Job enabled");
//    timer.run();
//  }
//  else if (Serial.read() == '#')
//  {
//      Serial.println("Job disabled");
//    timer.disable(timerId);
//  }
//}
//  Serial.print("Magnet Passes = ");
//  Serial.println(magnetPasses);
//  delay(5000);
}
