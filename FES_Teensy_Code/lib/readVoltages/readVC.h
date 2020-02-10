#ifndef readVC_h_
#define readVC_h_

#include <Arduino.h>
#include <SPI.h>
#include "definitions.h"
#include "readVC.h"
#include "globalVars.h"
#include "relayControl.h"

void ADCinternalSetup();
void FSRinit();
void readFSR();
void updateFSRStep();
void updateRelPV();

#endif