#ifndef definitions_h_
#define definitions_h_

/*
***DO NOT USE PINS 3,4,29,30 on Teensy 3.6***
These pins are used by TimerOne and TimerThree library


***USABLE GPIO PWM PINS***
2, 5, 6, 7, 8, 9, 10, 14, 16, 17, 20, 21, 22, 23, 35, 36, 37, 38


***ANALOG PINS***
ADC0:                               ADC1:
PIN     Analog                      PIN     Analog
14      A0                          31      A12
15      A1                          32      A13
16      A2                          33      A14
17      A3                          34      A15
18      A4                          35      A16
19      A5                          36      A17
20      A6                          37      A18
21      A7                          38      A19
22      A8                          39      A20
23      A9
*/

// hardware pin definitions
#define rel1resetPin    2   // relay 1 OFF pin (dorsal)
#define rel1setPin      3   // relay 1 ON pin  (dorsal)
#define rel2resetPin    4   // relay 2 OFF pin (plantar)
#define rel2setPin      5   // relay 2 ON pin  (plantar)
#define FSR1tPin        14  // adc0 to read fsr 1 toe pin
#define FSR1hPin        31  // adc1 to read fsr 1 heel pin
#define FSR2tPin        32  // adc1 to read fsr 2 toe pin
#define FSR2hPin        15  // adc0 to read fsr 2 heel pin
#define rel1onLED       20  // red closest to blue
#define rel1offLED      21  // green closest to blue
#define rel2onLED       23  // red furthest from blue
#define rel2offLED      22  // green furthest from blue
#define powerOnLED      19  // blue
#define chipSelect      BUILTIN_SDCARD

// timing definitions
#define dtLog           50 // milliseconds
#define dtControl       50  // period for control update
#define dtRead          50  // period for updating FSR readings
#define blinkyLED       200 // period for blinking the LED when GUI is not connected

/*
The mode and affectedInput does not impact the data logging.  This is useful in 
post processing where the phase variable can be validated for for future use.
*/

// control method
// 1 : Use FSR to control the relays
// 2 : Use the phase variable approximation to control the relay

#define Razor           Serial2
#define SerialOut       Serial

// Mask out the 6th bit (case in ASCII) to ignore case
#define ignoreCase(c) c & ~_BV(5)

#endif