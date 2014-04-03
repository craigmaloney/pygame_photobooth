#include <SoftwareSerial.h>


/*
  Button
 
 Turns on and off a light emitting diode(LED) connected to digital  
 pin 13, when pressing a pushbutton attached to pin 2. 
 
 
 The circuit:
 * LED attached from pin 13 to ground 
 * pushbutton attached to pin 2 from +5V
 * 10K resistor attached to pin 2 from ground
 
 * Note: on most Arduinos there is already an LED on the board
 attached to pin 13.
 
 
 created 2005
 by DojoDave <http://www.0j0.org>
 modified 30 Aug 2011
 by Tom Igoe
 
 This example code is in the public domain.
 
 http://www.arduino.cc/en/Tutorial/Button
 */

// constants won't change. They're used here to 
// set pin numbers:
const int buttonPin = 9;     // the number of the pushbutton pin
const int ledPin =  8;      // the number of the LED pin

// variables will change:
int buttonState = 0;         // variable for reading the pushbutton status
int counter = 0;
  
void setup() {
  Serial.begin(9600); 
  Serial.println("Arduino up");
  // initialize the LED pin as an output:
  pinMode(ledPin, OUTPUT);      
  // initialize the pushbutton pin as an input:
  pinMode(buttonPin, INPUT);     

}

void loop(){
  // read the state of the pushbutton value:
  buttonState = digitalRead(buttonPin);

  if (counter > 20000){
    digitalWrite(ledPin, LOW);
  } else {
    digitalWrite(ledPin, HIGH);
  }
  
  counter = counter + 1;
  if (counter > 60000){
    counter = 0;
  }
    
  // check if the pushbutton is pressed.
  // if it is, the buttonState is HIGH:
  if (buttonState == HIGH) {     
    // turn LED on:
    Serial.println("Pressed!");
    fire();
  }   
}

void fire(){
  for (int i = 0; i <= 2; i++) {
    digitalWrite(ledPin, LOW);
    delay(1000);
    digitalWrite(ledPin, HIGH);
    delay(100);
  }
  Serial.println("Fire!");
  delay(2000);
}

