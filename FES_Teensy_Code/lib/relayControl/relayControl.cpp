#include "relayControl.h"

void relayControl(int relay, int stat) {
    if (relay == 2) {
        // dorsal relay control
        if (stat == 1) {
            // relay 1 on
            digitalWrite(rel1resetPin, LOW);
            digitalWrite(rel1setPin, HIGH);
            rel1stat = true;

        } else if (stat == 0) {
            // relay 1 off
            digitalWrite(rel1setPin, LOW);
            digitalWrite(rel1resetPin, HIGH);
            rel1stat = false;
        }
    } else if (relay == 1) {
        // plantar relay control
        if (stat == 1) {
            // relay 2 on
            digitalWrite(rel2setPin, HIGH);
            digitalWrite(rel2resetPin, LOW);
            rel2stat = true;
        } else if (stat == 0) {
            // relay 2 off
            digitalWrite(rel2setPin, LOW);
            digitalWrite(rel2resetPin, HIGH);
            rel2stat = false;
        }
    } else if (relay == 3) {
        // turn both relays off
        digitalWrite(rel1resetPin, HIGH);
        digitalWrite(rel2resetPin, HIGH);
        rel1stat = false;
        rel2stat = false;
    }
    digitalWrite(rel1onLED, rel1stat);
    digitalWrite(rel1offLED, !rel1stat);
    digitalWrite(rel2onLED, rel2stat);
    digitalWrite(rel2offLED, !rel2stat);
}

