#ifndef dataLog_h_
#define dataLog_h_

#include <Arduino.h>
#include <SD.h>
#include "definitions.h"
#include "globalVars.h"
#include "dataManip.h"

class dataLog {
    private:
        String gyro;
        String accel;
        float phaseV;
        bool FSR1t;
        bool FSR1h;
        bool FSR2t;
        bool FSR2h;
        bool rel1;
        bool rel2;
        unsigned long int tStamp;

    public:
        File dataFile_;
        File logFile_;
        void setupSD();
        void syncReadings(unsigned long int t);
        void logOut();
        void closeFile();
        void updateExpNum(int exp);
};

#endif