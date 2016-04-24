// Setup HTU21D humidity and temp sensor
#include <Wire.h>
#include "HTU21D.h"
#include "Adafruit_LiquidCrystal.h"
#include <SoftwareSerial.h>

HTU21D myHumidity;

Adafruit_LiquidCrystal lcd(0);

// Setup NTC 3950 100K thermistor
// which analog pin to connect
#define THERMISTORPIN A0         
// resistance at 25 degrees C
#define THERMISTORNOMINAL 100000      
// temp. for nominal resistance (almost always 25 C)
#define TEMPERATURENOMINAL 25   
// how many samples to take and average, more takes longer
// but is more 'smooth'
#define NUMSAMPLES 5
// The beta coefficient of the thermistor (usually 3000-4000)
#define BCOEFFICIENT 3950
// the value of the 'other' resistor
#define SERIESRESISTOR 100000    
#define HEATERBED 4    

boolean HEATERBED_STATE_ON = false;

int tempSetting = 70;

int samples[NUMSAMPLES];
 
void setup(void) {
  pinMode(HEATERBED, OUTPUT);
  
  Serial.begin(9600);
//  Serial.println("Temperature Tracker Started!");
  analogReference(EXTERNAL);
  myHumidity.begin();
  lcd.begin(16, 2);
//  lcd.print("Initialization...");
}
 
void loop(void) {
//    lcd.clear();
     lcd.setCursor (0,1);    
//  float humd = myHumidity.readHumidity();
  float temp = myHumidity.readTemperature();

  if(Serial.available())
  {
    byte incoming = Serial.read();

    if(incoming == '!')
    {
      changeState();
    }
    else if(incoming == '#')
    {
      changeState();
    }
  }

  
  uint8_t i;
  float average;
 
  // take N samples in a row, with a slight delay
  for (i=0; i< NUMSAMPLES; i++) {
   samples[i] = analogRead(THERMISTORPIN);
   delay(10);
  }
 
  // average all the samples out
  average = 0;
  for (i=0; i< NUMSAMPLES; i++) {
     average += samples[i];
  }
  average /= NUMSAMPLES;
 
//  Serial.print("Average analog reading "); 
//  Serial.println(average);
 
  // convert the value to resistance
  average = 1023 / average - 1;
  average = SERIESRESISTOR / average;
//  Serial.print("Thermistor resistance "); 
//  Serial.println(average);
 
  float steinhart;
  float steinhartF;
  steinhart = average / THERMISTORNOMINAL;     // (R/Ro)
  steinhart = log(steinhart);                  // ln(R/Ro)
  steinhart /= BCOEFFICIENT;                   // 1/B * ln(R/Ro)
  steinhart += 1.0 / (TEMPERATURENOMINAL + 273.15); // + (1/To)
  steinhart = 1.0 / steinhart;                 // Invert
  steinhart -= 273.15;                         // convert to C
  steinhartF = (steinhart * 1.8) + 32;
 
//  Serial.print("Thermistor Temperature: "); 
    Serial.println(steinhart);
//  Serial.print("HTU21D Temperature: ");
//  Serial.println(temp, 1);
//  Serial.println();
  
//  Serial.println(" *C");

    lcd.setCursor(0, 0);
    lcd.print("Set: ");
    lcd.print(tempSetting);
    lcd.print(" C");
    
    lcd.setCursor(13, 0);
    if(HEATERBED_STATE_ON) {
    lcd.print(" ON");
    }
    else if(!HEATERBED_STATE_ON) {
    lcd.print("OFF");
    }
    
    lcd.setCursor(0, 1);
    lcd.print(steinhart);
    lcd.print(" C  ");
    lcd.print(steinhartF);
    lcd.print(" F");
  delay(1000);
}

void changeState()
{
  if(HEATERBED_STATE_ON)
  {
  digitalWrite(HEATERBED, LOW);
  Serial.println("Heater OFF");
  HEATERBED_STATE_ON = false;
  }
  else if(!HEATERBED_STATE_ON)
  {
  digitalWrite(HEATERBED, HIGH);
  Serial.println("Heater ON");
  HEATERBED_STATE_ON = true;
  }
}

