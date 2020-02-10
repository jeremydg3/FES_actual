#ifndef relayControl_h_
#define relayControl_h_

#include <Arduino.h>
#include "definitions.h"
#include "globalVars.h"

void relayControl(int relay, int stat);
void LEDcontrol();

#endif