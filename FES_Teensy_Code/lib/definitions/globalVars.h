#ifndef globalVars_h_
#define globalVars_h_

#include <Arduino.h>
#include "definitions.h"

// fsr reading and thresholds
extern float fsr[4];
extern float fsrThresh[4];
extern bool fsrFlag[4];
extern bool fsrFlagPrev[4];
extern bool fsrStep[4][2];
extern int fsrStepC;
extern int toeIndx;
extern int heelIndx;

// String parsing data
extern float phaseVar;

// variables for relay control
extern bool rel1stat;
extern bool rel2stat;

// fsr threshold met variables
extern bool FSR_h1;
extern bool FSR_t1;
extern bool FSR_h2;
extern bool FSR_t2;
extern int relT;

// variables for timing
extern unsigned long int currT;
extern unsigned long int prevT;
extern unsigned long int deltaC;
extern unsigned long int deltaL;
extern unsigned long int deltaR;
extern int fade;

// razor data parsing variables
extern int ind1, ind2, ind3, pind;
extern String A, G;

// experiment data logging
extern int expNum;
extern String expTitle;
extern bool sdLog;
extern bool sdWorking;
extern int state;
extern int controlMethod;
extern bool controlState;
extern int affectedInput;

#endif