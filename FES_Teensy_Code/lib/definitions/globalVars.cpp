#include "GlobalVars.h"

// fsr reading and thresholds
float fsr[4];
float fsrThresh[4];
bool fsrFlag[4];
bool fsrFlagPrev[4];
bool fsrStep[4][2];
int fsrStepC;
int toeIndx = 0;
int heelIndx = 0;

// String parsing data
float phaseVar;

// variables for relay control
bool rel1stat = false;
bool rel2stat = false;

// fsr threshold met variables
bool FSR_h1 = false;
bool FSR_t1 = false;
bool FSR_h2 = false;
bool FSR_t2 = false;

// variables for timing
//unsigned long int currT = 0;
//unsigned long int prevT = 0;
unsigned long int deltaC = 0;
unsigned long int deltaL = 0;
unsigned long int deltaR = 0;
int fade = 0;

// razor data parsing variables
int ind1, ind2, ind3, pind;
String A, G;

// experiment data logging
int expNum = 0;
String expTitle = "";
bool sdLog = false;
bool sdWorking = false;
int state = 0;
int controlMethod = 0; // 0: FSR, 1: phase Variable
bool controlState = false;
int affectedInput = 1; // 1:Left , 2:Right
