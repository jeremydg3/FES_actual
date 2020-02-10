#include "dataManip.h"

// converts string to integer
int strToInt(String in) {
  int num = 0;
  for (unsigned int i = 0; i < in.length(); i++) {
    num = num * 10 + in.charAt(i) - '0';
  }
  return num;
}

// converts string to floating point value
float strToFloat(String in) {
  float numWhole = 0.0;
  float numDecim = 0.0;
  float numOut = 0.0;
  int inLength = in.length();
  bool decimal = false;
  bool neg = false;
  for (int i = 0; i < inLength; i++) {
    if (in.charAt(i) == '-') {
      neg = true;
    }
  }
  for (int i = 0; i < inLength; i++) {
    if (in.charAt(i) == '.') {
      decimal = true;
      break;
    }
    numWhole = numWhole * 10 + in.charAt(i) - '0'; 
  }
  if (decimal) {
    for (int i = inLength - 1; i >= 0; i--) {
      if (in.charAt(i) == '.') {
        break;
      } else {
        numDecim = numDecim * 0.1 + in.charAt(i) - '0';
      }
    }
  }
  numOut = numWhole + numDecim*0.1;
  if (neg)
    numOut = -numOut;
  return numOut;
}