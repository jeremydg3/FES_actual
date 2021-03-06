/*******************************************************************
** FILE:
**    Common_Config.h
** DESCRIPTION:
**    Header containing IMU definitions which are platform agnostic.
**    Definitions in this file should be independent of IMU version.
********************************************************************/
#ifndef COMMON_CONFIG_H
#define COMMON_CONFIG_H



/* 0: IMU
** 1: Emulator */
#define EXE_MODE 0

//#define _IMU10736_ /* Using IMU10736 */
#define _IMU9250_ /* Using IMU9250 */

#define DEBUG 1 /* Print log/verbose information */

#if EXE_MODE==1
  /* Emulator (C,Offline) mode */
  #include <math.h>
  #include <stdio.h>
  #include <stdio.h>
  #include <inttypes.h>
  #include <stdbool.h>
  #include <string.h>
  #include <time.h>
  
  #include "../Include/Common_Types.h"
  #include "../Include/Math.h"
  #include "../Include/Calibration_Config.h"
  #include "../Include/DSP_Config.h"
  #include "../Include/DCM_Config.h"
  #include "../Include/GaPA_Config.h"
  #include "../Include/WISE_Config.h"
  #include "../Include/Communication_Config.h"
  #include "../Include/Log_Config.h"


  #include "../Include/Emulator_Config.h"

  #ifdef _IMU10736_
    #include "../Include/IMU10736_Config.h"
  #endif
  #ifdef _IMU9250_
    #include "../Include/IMU9250_Config.h"
  #endif

#else
  /* IMU mode */
  #include "./Common_Types.h"
  #include "./Calibration_Config.h"
  #include "./DSP_Config.h"
  #include "./DCM_Config.h"
  #include "./GaPA_Config.h"
  #include "./WISE_Config.h"
  #include "./Communication_Config.h"
  #include "./Math.h"
  #include "./Log_Config.h"

  #ifdef _IMU10736_
    #include "./IMU10736_Config.h"
  #endif
  #ifdef _IMU9250_
    //#include <SparkFunMPU9250-DMP.h>
    #include "./IMU9250_Config.h"
  #endif
#endif




/**********************
** These are defaults,
** Future releases are intended to have the ability to
** hot switch these. */

/* I/O params */
#define OUTPUT_MODE 1
#define NUM_COM_MODES 2

/* Calibration params  */
#define CALIBRATION_MODE  0 /* 0:OFF 1:ON */
#define CAL_OUTPUT_MODE 0
#define NUM_CALCOM_MODES 1

/* Default Algorithms */
#define DCM_ON 1
#define DSP_ON 1
#define GAPA_ON 1
#define WISE_ON 0

/* Set which sensors to read */
#define ACCEL_ON 1
#define GYRO_ON  1
#define MAGN_ON  0 /* We removed support for the mag in the DCM! */


/*******************************************************************
** Typedefs *********************************************************
********************************************************************/


/*
** TYPE: SENSOR_STATE_TYPE
** This type is used to hold the sensor
** variables */
typedef struct
{
  SAMPLE_DATA_1D_TYPE yaw;
  SAMPLE_DATA_1D_TYPE pitch;
  SAMPLE_DATA_1D_TYPE roll;

  /* Accel x:Fore y:Port z:Zenith */
  SAMPLE_DATA_2D_TYPE accel;
  SAMPLE_DATA_2D_TYPE gyro;
  SAMPLE_DATA_2D_TYPE magn; /* not used */
  
} SENSOR_STATE_TYPE;

/*
** TYPE: SENSOR_PRMS_TYPE
** This type is used to hold the
** Sensor specific parameters */
typedef struct
{
  int gravity;

  int accel_on;
  int gyro_on;
  int magn_on;

  int sample_rate;

} SENSOR_PRMS_TYPE;




/*
** TYPE: CONTROL_TYPE
** This type is used to hold all the execution
** parameters. It allows for a more dynamic
** execution. */
typedef struct
{
  /* Full count of number of samples */
  unsigned long int SampleNumber;
  bool SampleNumberOverflow;
  
  /* Common exe parameters */
  unsigned long timestamp;
  unsigned long timestamp_old;
  float G_Dt;

  /* If in Emulation mode,
  ** include the emulation structure */
  #if EXE_MODE==1
    EMULATION_TYPE emu_data;
    META_PACKET_TYPE meta_packet;
  #endif



  /* Serial communication variables */
  int      output_mode;
  bool     BaudLock;    /* Used to set baud rate */
  uint32_t LastLogTime; /* Sets the UART LOG Rate */
  /* LED state globals */
  bool     LedState; /* Used to set LED state */
  uint32_t LastBlinkTime; /* Used to set LED state */
  
  
  /* SD controls */
  bool     SDCardPresent;
  
  /* Log Info File (text w/ dbug info) */
  OUTPUT_LOG_FILE_TYPE log_info_file;
  /* Log Data File (binary data only w/ meta header) */
  OUTPUT_LOG_FILE_TYPE log_data_file;

  int verbose;
  int calibration_on;
  int DCM_on;
  int DSP_on;
  int GaPA_on;
  int WISE_on;

  /* Sensor specific parameters */
  SENSOR_PRMS_TYPE sensor_prms;

  /* Digital Signal Processing parameters */
  DSP_PRMS_TYPE dsp_prms;

  /* DCM parameters */
  DCM_PRMS_TYPE dcm_prms;

  /* GaPA parameters */
  GAPA_PERMS_TYPE gapa_prms;

  /* WISE parameters */
  WISE_PRMS_TYPE wise_prms;

  /* If calibration mode,
  ** include calibration struct */
  CALIBRATION_PRMS_TYPE calibration_prms;

} CONTROL_TYPE;








#endif /* End COMMON_CONFIG_H */
