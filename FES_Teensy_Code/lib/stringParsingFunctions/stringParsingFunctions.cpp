#include <stringParsingFunctions.h>

// reads and parses the data read from the Razor IMU.  First an empty '\n' is sent to the IMU
// which then prompts a response from the IMU where accelerometer, gyroscope, and phase variable
// data is sent back to the Teensy
void parseRazorIn() {
  Razor.println();
  if (Razor.available() > 0) {
    String razorData = Razor.readStringUntil('\n');
    razorData = Razor.readStringUntil('\n');
    // SerialOut.println(razorData);
    ind1 = razorData.indexOf(';');
    A = razorData.substring(0, ind1);
    
    ind2 = razorData.indexOf(';', ind1 + 1);
    G = razorData.substring(ind1 + 1, ind2 + 1);

    ind3 = razorData.indexOf(';', ind2 + 1);
    phaseVar = razorData.substring(ind2 + 1).toFloat();
  }
  // SerialOut.println(phaseVar,3);
}

/*
1) GUI sends '1' to handshake and send Teensy to standby
2) GUI sends '2' to go to trial mode
3) GUI sends '3' to go to relay control [debug] mode
We can only transition to each mode from state 1 [standby]
*/
// string parsing when user enters new command
void stateParse(String in, dataLog data) {
  // SerialOut.print("in:    ");
  // SerialOut.println(in);
  switch(in.charAt(0)) {
    case '0':
      state = 0;
      sdLog = false;
      break;
    case '1':
      //SerialOut.println("GUI connected");
      state = 1;
      sdLog = false;
      break;
    case '2':
      //SerialOut.println("trial mode");
      if (state == 1)
        state = 2;
        // if we have already received a '2' from the GUI, 
        // and if there is more in the command string 
        // change the control method or start/end trial
        // EX: 20 is FSR, 21 is phase variable
        if (in.length() > 1) {
          switch(in.charAt(1)) {
            case 's':
              // start trial
              data.setupSD();
              data.updateExpNum(expNum);
              sdLog = true;
              controlState = true;
              break;
            case 'e':
              // end trial
              sdLog = false;
              controlState = false;
              break;
            case 'a':
              // set the affected input
              affectedInput = in.charAt(2) - '0';
              if (affectedInput == 1) {
                toeIndx = 0;
                heelIndx = 1;
              } else if (affectedInput == 2){
                toeIndx = 2;
                heelIndx = 3;
              }
              break;
            default:
              controlMethod = in.charAt(1) - '0';
              break;
          }
        }
      break;

    case '3':
      //SerialOut.println("relay control mode");
      if (state == 1)
        state = 3;
        sdLog = false;
        if (in.length() > 1) {
          // if we have already received a '3' from the GUI, 
          // and if there is more in the command string 
          // flip the appropriate relay
          // EX: 311 turns relay 1 (dorsal) ON, 320 turns relay 2 (plantar) OFF
          relayControl(in.charAt(1) - '0', in.charAt(2) - '0');
        }
      break;
  }
}