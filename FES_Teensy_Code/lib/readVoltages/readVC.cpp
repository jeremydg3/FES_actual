#include <readVC.h>
#include <ADC.h>

ADC *adc = new ADC();

/* 
ADCinternalSetup() sets up the internal ADC on the Teensy.
  - sets the reference voltage for both onboard ADC
  - sets the resolution to be the max of 13 bits
*/
void ADCinternalSetup() {
  adc->setResolution(12, ADC_0);
  adc->setResolution(12, ADC_1);
}

void FSRinit() {
  // [0] 30-50     - toe
  // [1] 50 - 70   - heel
  // [2] 75 - 100  - toe
  // [3] 250 - 300 - heel
  fsrThresh[0] = 450;
  fsrThresh[1] = 500;
  fsrThresh[2] = 350;
  fsrThresh[3] = 120;

  fsrStep[0][0] = 1; fsrStep[0][1] = 1;
  fsrStep[1][0] = 1; fsrStep[1][1] = 0;
  fsrStep[2][0] = 0; fsrStep[2][0] = 0;
  fsrStep[3][0] = 0; fsrStep[3][1] = 1;

  for (int i = 0; i < 4; i++) {
    fsrFlag[i] = false;
    fsrFlagPrev[i] = false;
  }
  fsrStepC = 0;
}


/* 
readLowSide() stores analog readings from the Teensy's onboard ADCs.
  - Teensy3.6 ADC is set to max(13-bit) resolution in setup
  - moving average of [samples] size
  - lvrRaw stores raw values for debugging
  - lvrMap stores mapped values to the reference voltage
*/
void readFSR() {
  // read in new values
  ADC::Sync_result reading1 = adc->analogSyncRead(FSR1tPin, FSR1hPin);
  fsr[0] = reading1.result_adc0;
  fsr[1] = reading1.result_adc1;
  ADC::Sync_result reading2 = adc->analogSyncRead(FSR2hPin, FSR2tPin);
  fsr[2] = reading2.result_adc0;
  fsr[3] = reading2.result_adc1;

  // 1 is on
  // 0 is off
  for (int i = 0; i < 4; i++) {
    if (fsr[i] < fsrThresh[i]) {
      fsrFlag[i] = 1;
    } else {
      fsrFlag[i] = 0;
    }
  }
}

void updateRelPV() {
  if ((phaseVar >= 0 && phaseVar < 0.4)) {
    relayControl(3, 0);
  } else if ((phaseVar >= 0.4 && phaseVar < 0.6)) {
    // toes pushing off
    relaycontrol(2, 0);
    relayControl(1, 1);
  } else if ((phaseVar >= 0.6 && phaseVar < 1.0)) {
    // toes up
    relayControl(1, 0);
    relayControl(2, 1);
  }
}

void updateFSRStep() {
  if (fsrFlag[toeIndx] != fsrFlagPrev[toeIndx] || fsrFlag[heelIndx] != fsrFlagPrev[heelIndx]) {
    fsrFlagPrev[toeIndx] = fsrFlag[toeIndx];
    fsrFlagPrev[heelIndx] = fsrFlag[heelIndx];
    if (fsrStepC == 4) {
        fsrStepC = 0;
      }

    // if both are different than the previous flag, check if they match the next step 
    if (fsrFlag[toeIndx] == fsrStep[fsrStepC][0]) {
      if (fsrFlag[heelIndx] == fsrStep[fsrStepC][1]) {
        // if they match the next step then increase fsrStepC
        switch(fsrStepC) {
          case 0:
            relayControl(3,0);
            break;
          case 1:
            relayControl(2, 0);
            relayControl(1, 1);
            break;
          case 2:
            relayControl(1, 0);
            relayControl(2, 1);
            break;
          case 3:
            relayControl(3, 0);
            break;
        }
        fsrStepC+=1;
      }
    }
  }
}