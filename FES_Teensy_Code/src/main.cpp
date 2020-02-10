#include <Arduino.h>
#include <definitions.h>
#include <globalVars.h>
#include <dataManip.h>
#include <dataLog.h>
#include <stringParsingFunctions.h>
#include <relayControl.h>
#include <readVC.h>
#include <timers.h>

// create data log object
dataLog data;

// create timer objects
timer loggingTimer;
timer controlTimer;
timer readingTimer;
timer trialLEDTimer;
timer standbyLEDTimer;
timer relayLEDTimer;

int dif = 0;

// function prototypes
void serialEvent();
void updateTimer();
void statusLED(int state);
void updateMillisT(unsigned long int t);

void setup() {
  // set pinModes
  pinMode(rel1setPin, OUTPUT);
  pinMode(rel1resetPin, OUTPUT);
  pinMode(rel2setPin, OUTPUT);
  pinMode(rel2resetPin, OUTPUT);
  pinMode(FSR1tPin, INPUT);
  pinMode(FSR1hPin, INPUT);
  pinMode(FSR2tPin, INPUT);
  pinMode(FSR2hPin, INPUT);
  pinMode(rel1onLED, OUTPUT);
  pinMode(rel1offLED, OUTPUT);
  pinMode(rel2onLED, OUTPUT);
  pinMode(rel2offLED, OUTPUT);
  pinMode(powerOnLED, OUTPUT);

  // initialize timer objects and add new timers for logging, 
  // stim control and reading values (ms) <defined in definitions.h>
  loggingTimer.initTimer(dtLog);
  controlTimer.initTimer(dtControl);
  readingTimer.initTimer(dtRead);
  trialLEDTimer.initTimer(750);
  standbyLEDTimer.initTimer(blinkyLED);
  relayLEDTimer.initTimer(20);

  
  // setup the onboard ADC for use
  ADCinternalSetup();

  // set up fsr readings
  FSRinit();

  // begin Serial for COM
  SerialOut.begin(9600);
  delay(50);

  // begin Serial 1 for Razor
  Razor.begin(115200);
  delay(50);

  // set relays to be off
  relayControl(1,0);
  relayControl(2,0);

  // wait until the Razor is ready
  while(1) {
    Razor.println();
    if (Razor.available() > 0) break;
  }
  // setup SD card 
  //data.setupSD();
}

/* FSR control phases go as follows

Heel  |  Toe  |   Muscle Stim
------|-------|---------------
  ON  |  ON   |   BOTH OFF 
  OFF |  ON   |  PF-ON   DF-OFF
  OFF |  OFF  |  PF-OFF  DF-ON
  ON  |  OFF  |  PF-OFF  DF-OFF

Begin loop again
*/

void loop() {
  // update timestamp
  updateMillisT(millis());

  // update the status (blue) LED depending on the state we are currently in
  statusLED(state);

  // read and update FSR state (HIGH or LOW), update the phase variable form Razor
  if (readingTimer.checkTimer()) {
    readFSR();
    parseRazorIn();
  }
  // update the logging values and log to the Serial port or the microSD card
  if (loggingTimer.checkTimer()) {
    data.syncReadings(millis());
  }

  // FES mode
  if (state == 2) {
    // set the relay status using defined control method
    if (controlTimer.checkTimer() && controlState) {
      if (controlMethod == 1) {
        // use FSR values to update the relay status'
        updateFSRStep();
      } else if (controlMethod == 2) {
        // use phase variable to update the relay status'
        updateRelPV();
      }
    }
  }
}

void serialEvent() {
  while (SerialOut.available() > 0) {
    String in = SerialOut.readStringUntil('\n');
    stateParse(in, data);
    SerialOut.println(state);
  }
}

void statusLED(int state) {
  switch (state) {
    case 0:
      // power is on but no GUI connected
      //  * blue led blinks quickly
      if (standbyLEDTimer.checkBool()) {
        digitalWrite(powerOnLED, HIGH);
      } else {
        digitalWrite(powerOnLED, LOW);
      }
      break;

    case 1:
      // connected to GUI and waiting to start trial or relay control mode
      //  * solid blue
      digitalWrite(powerOnLED, HIGH);
      break;
    
    case 2:
      // trial mode
      //  * blue led blinks slowly
      if (trialLEDTimer.checkBool()) {
        digitalWrite(powerOnLED, HIGH);
      } else {
        digitalWrite(powerOnLED, LOW);
      }
      break;

    case 3:
      // relay control mode
      // * blue LED fades on and off
      // if (fade == 0) {
      //   dif = 1;
      // } else if (fade == 255) {
      //   dif = -1;
      // }
      // if (relayLEDTimer.checkTimer()) {
      //   SerialOut.println(fade);
      //   fade+=dif;
      //   analogWrite(powerOnLED, fade);
      // }
      break;
  }
}

void updateMillisT(unsigned long int t) {
  loggingTimer.millisT = t;
  controlTimer.millisT = t;
  readingTimer.millisT = t;
  trialLEDTimer.millisT = t;
  standbyLEDTimer.millisT = t;
  relayLEDTimer.millisT = t;
}