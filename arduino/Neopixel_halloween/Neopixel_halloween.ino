// NeoPixel Ring simple sketch (c) 2013 Shae Erisson
// released under the GPLv3 license to match the rest of the AdaFruit NeoPixel library

#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
  #include <avr/power.h>
#endif

// Which pin on the Arduino is connected to the NeoPixels?
// On a Trinket or Gemma we suggest changing this to 1
#define PIN            6

// How many NeoPixels are attached to the Arduino?
#define NUMPIXELS      5
#define MAX_BRIGHTNESS      255
#define LOOPCOUNT      50
#define LOOP      1

// When we setup the NeoPixel library, we tell it how many pixels, and which pin to use to send signals.
// Note that for older NeoPixel strips you might need to change the third parameter--see the strandtest
// example for more information on possible values.
Adafruit_NeoPixel pixels = Adafruit_NeoPixel(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

int delayval = 10; // delay for half a second

void setup() {
  pixels.begin(); // This initializes the NeoPixel library.
}

void loop() {

  // For a set of NeoPixels the first NeoPixel is 0, second is 1, all the way up to the count of pixels minus one.
  // RED = 255,0,0          x,0,0
  // ORANGE = 255,127,0  x,x/2.007874,0
  // YELLOW = 255,255,0      x,x,0
  // GREEN = 0,255,0        0,x,0
  // BLUE = 0,0,255         0,0,x
  // PURPLE = 128,0,128  x/1.99,0,x/1.99


for(int n=0;n<=1;n++)
{

  for(int a=0;a<=MAX_BRIGHTNESS;a++)
    {
    // pixels.Color takes RGB values, from 0,0,0 up to 255,255,255
    pixels.setPixelColor(0, pixels.Color(0,0,a)); // Red
    pixels.setPixelColor(1, pixels.Color(0,0,a)); // Orange

    pixels.show(); // This sends the updated pixel color to the hardware.

    delay(delayval); // Delay for a period of time (in milliseconds).
    }

  for(int b=MAX_BRIGHTNESS;b>=0;b--)
    {
    // pixels.Color takes RGB values, from 0,0,0 up to 255,255,255
    pixels.setPixelColor(0, pixels.Color(0,0,b)); // Moderately bright green color.
    pixels.setPixelColor(1, pixels.Color(0,0,b)); // Moderately bright green color.

    pixels.show(); // This sends the updated pixel color to the hardware.

    delay(delayval); // Delay for a period of time (in milliseconds).
    }
    
    delay(2000);
}

    for(int c=0;c<10;c++)
    {
    // pixels.Color takes RGB values, from 0,0,0 up to 255,255,255
    pixels.setPixelColor(0, pixels.Color(0,255,0)); // Red
    pixels.setPixelColor(1, pixels.Color(0,255,0)); // Orange

    pixels.show(); // This sends the updated pixel color to the hardware.
    delay(500); // Delay for a period of time (in milliseconds).

    // pixels.Color takes RGB values, from 0,0,0 up to 255,255,255
    pixels.setPixelColor(0, pixels.Color(255,127,255,0)); // Moderately bright green color.
    pixels.setPixelColor(1, pixels.Color(255,127,0)); // Moderately bright green color.

    pixels.show(); // This sends the updated pixel color to the hardware.

    delay(500); // Delay for a period of time (in milliseconds).

    // pixels.Color takes RGB values, from 0,0,0 up to 255,255,255
    pixels.setPixelColor(0, pixels.Color(128,0,128)); // Moderately bright green color.
    pixels.setPixelColor(1, pixels.Color(128,0,128)); // Moderately bright green color.

    pixels.show(); // This sends the updated pixel color to the hardware.

    delay(500); // Delay for a period of time (in milliseconds).
    }
    
    delay(2000);

}
