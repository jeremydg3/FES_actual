#include "dataLog.h"

// sets up the SD card and file usage, **ONLY GETS CALLED ONCE IN SETUP**
void dataLog::setupSD() {
    // SD card initialization
    sdWorking = false;
    if (SD.begin(chipSelect)) {
        // SD card initialized and working
        sdWorking = true;
        // update the logFile which logs the experiment number
        if (SD.exists("logFile.txt")) {
            logFile_ = SD.open("logFile.txt");
            String in = "";
            while(logFile_.available()) {
                int n = logFile_.read();
                if (n != 10) {
                    if (47 < n && n < 58){ in += (char)n; }
                } else {
                    // updates the current experiment number being run
                    expNum = strToInt(in);
                    in = "";
                }
            }
            SerialOut.println(expNum);
            logFile_.close();
        }
    }
}

/*
updateExpNum(int exp) updates the experiment number to be saved to the SD card
and updates the header and file name for the file
*/
void dataLog::updateExpNum(int exp) {
    if (sdWorking) {
        expNum++;
        expTitle = "E";
        expTitle += String(expNum) + ".txt";
        const char * fname = expTitle.c_str();

        // update experiment title and header for the data file
        dataFile_ = SD.open(fname, FILE_WRITE);
        dataFile_.print("-> Data should be recorded every ");
        dataFile_.print(dtLog);
        dataFile_.println(" milliseconds\n");
        dataFile_.print("-> Affected Limb [1:Left , 2:Right]:         ");
        dataFile_.println(affectedInput);
        dataFile_.print("-> Relay control [1:FSR , 2:Phase Variable]: ");
        dataFile_.println(controlMethod);
        dataFile_.print("\ntimestamp[ms]");
        dataFile_.print(',');
        dataFile_.print("gyro");
        dataFile_.print(',');
        dataFile_.print("accel");
        dataFile_.print(',');
        dataFile_.print("phaseV");
        dataFile_.print(',');
        dataFile_.print("FSR1toe");
        dataFile_.print(',');
        dataFile_.print("FSR1heel");
        dataFile_.print(',');
        dataFile_.print("FSR2toe");
        dataFile_.print(',');
        dataFile_.print("FSR2heel");
        dataFile_.print(',');
        dataFile_.print("Dorsal Relay");
        dataFile_.print(',');
        dataFile_.println("Plantar Relay");
        dataFile_.close();
        // update experiment number on the experiment logging file
        logFile_ = SD.open("logFile.txt", FILE_WRITE);
        logFile_.println(expNum);
        logFile_.close();
    }
}

/*
syncReadings() computes the current at the battery output, HV dcdc converter
input, and HV dcdc converter output, and synchronizes all voltage/status values
*/
void dataLog::syncReadings(unsigned long int t) {
    // noInterrupts() ensures that we are using the same values every time we log data
    // this synchronizes the output to the SD card and Serial
    noInterrupts();
    
    // store voltage
    // store raw values for logging
    gyro = G;
    accel = A;
    phaseV = phaseVar;
    FSR1t = fsrFlag[0];
    FSR1h = fsrFlag[1];
    FSR2t = fsrFlag[2];
    FSR2h = fsrFlag[3];
    rel1 = rel1stat;
    rel2 = rel2stat;
    tStamp = t;

    interrupts();
    logOut();
}

/*
timeStamp
gyro
accel
phaseV
FSR1t
FSR1h
FSR2t
FSR2h
relay1stat
relay2stat
*/
/*
writeToSD() logs data to the SD card and/or Serial
*/
void dataLog::logOut() {
    // storing data on the SD card
    if (sdLog && sdWorking) {
        const char * fname = expTitle.c_str();
        File dataFile_ = SD.open(fname, FILE_WRITE);
        dataFile_.print(tStamp);        // timestamp
        dataFile_.print(',');
        dataFile_.print(gyro);          // gyro values from Razor IMU
        dataFile_.print(',');
        dataFile_.print(accel);         // accel values from Razor IMU
        dataFile_.print(',');
        dataFile_.print(phaseV);        // phase variable from Razor IMU
        dataFile_.print(',');
        dataFile_.print(FSR1t);         // state of FSR1 (toe)
        dataFile_.print(',');
        dataFile_.print(FSR1h);         // state of FSR1 (heel)
        dataFile_.print(',');
        dataFile_.print(FSR2t);         // state of FSR2 (toe)
        dataFile_.print(',');
        dataFile_.print(FSR2h);         // state of FSR2 (heel)
        dataFile_.print(',');
        dataFile_.print(rel1stat);      // relay 1 status
        dataFile_.print(',');
        dataFile_.println(rel2stat);    // relay 2 status
        dataFile_.close();
    }

    SerialOut.print(gyro);           // gyro values from Razor IMU
    SerialOut.print(accel);          // accel values from Razor IMU
    SerialOut.print(';');
    SerialOut.print(phaseV);         // phase variable from Razor IMU
    SerialOut.print(';');
    SerialOut.print(FSR1t);          // state of FSR1 (toe)
    SerialOut.print(',');
    SerialOut.print(FSR1h);          // state of FSR1 (heel)
    SerialOut.print(',');
    SerialOut.print(FSR2t);          // state of FSR2 (toe)
    SerialOut.print(',');
    SerialOut.print(FSR2h);          // state of FSR2 (heel)
    SerialOut.print(',');
    SerialOut.print(rel1stat);       // relay 1 status
    SerialOut.print(',');
    SerialOut.print(rel2stat);       // relay 2 status
    SerialOut.print(',');
    if (sdLog && sdWorking) {
        SerialOut.print('1');
    } else {
        SerialOut.print('0');
    }
    SerialOut.print(',');
    SerialOut.println(state);        // current state
}