#ifndef stringParsingFunctions_h_
#define stringParsingFunctions_h_

#include <Arduino.h>
#include "definitions.h"
#include "globalVars.h"
#include "dataLog.h"
#include "relayControl.h"
#include "dataManip.h"

void parseRazorIn();
void stateParse(String in, dataLog data);

#endif