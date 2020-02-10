#ifndef timers_H
#define timers_H

#include <Arduino.h>
#include "globalVars.h"
#include "definitions.h"

class timer {
    private:
        bool timerFlag;
        unsigned long int timerDt;
        unsigned long int dt;
        
    public:
        unsigned long int millisT;
        void initTimer(int t);
        bool checkTimer();
        bool checkBool();
        
};

#endif