#include "timers.h"


// creates the timerDt variable for the specified timer
void timer::initTimer(int t) {
    timerFlag = false;
    timerDt = t/2;
}

// checks the timer once, best used for things that only require 
// checking once every 'timerDt' period
bool timer::checkTimer() {
    dt = millisT % (timerDt*2);
    if (dt < timerDt && !timerFlag) {
        timerFlag = true;
        return true;
    } else if (dt < timerDt && timerFlag) {
        return false;
    } else {
        timerFlag = false;
        return false;
    }
}

// really basic timer that returns true whenever the time is in the 
// predefined dt period, best for blinking an LED
bool timer::checkBool() {
    dt = millisT % (timerDt*2);
    if (dt < timerDt) {
        return true;
    } else {
        return false;
    }
}