/*******************************************************************
** FILE:
**    Logging_Functions
** DESCRIPTION:
**    This file contains the logging functions.
**    These functions are used exclusively in debug mode
**    and should not be included in the final firmware
**    implementation.
**    These functions are inteded for emulation
**    or debug modes only.
********************************************************************/


/*******************************************************************
** Includes ********************************************************
********************************************************************/

#ifndef COMMON_CONFIG_H
  #include "../Include/Common_Config.h"
#endif
#if EXE_MODE==1 /* Emulator Mode */
  /* In emulatiom mode, "Emulator_Protos" is needed to
  ** use funcitons in other files.
  ** NOTE: This header should contain the function
  **       prototypes for all execution functions */
  #include "../Include/Emulator_Protos.h"
#endif  /* End Emulator Mode */

/*******************************************************************
** Functions *******************************************************
********************************************************************/

/*************************************************
** FUNCTION: Meta_LogOut
** VARIABLES:
**    [I ]  CONTROL_TYPE      *p_control
**    [I ]  SENSOR_STATE_TYPE *p_sensor_state
**    [I ]  GAPA_STATE_TYPE   *p_gapa_state
**    [I ]  WISE_STATE_TYPE   *p_wise_state
** RETURN:
**    NONE
** DESCRIPTION:
**    This function will pack and write the meta data 
**    Header block.
**    
*/
void Meta_LogOut( CONTROL_TYPE       *p_control,
                  SENSOR_STATE_TYPE  *p_sensor_state,
                  GAPA_STATE_TYPE    *p_gapa_state,
                  WISE_STATE_TYPE    *p_wise_state)
{
  META_PACKET_TYPE Packet;
  
  float platform;
  float Default = -999;
    
  /* Get Platform */
  #ifdef _IMU10736_
    platform = 10736;
  #endif
  #ifdef _IMU9250_
    platform = 9250;
  #endif
  
  switch(DATA_PACKET_VERSION)
  {
    case 1 :
      Packet.version_id                     = (float)DATA_PACKET_VERSION;
      Packet.header_length                  = (float)sizeof(META_PACKET_TYPE);
      Packet.collection_id                  = Default; /* Post - Processing */
      Packet.collection_date                = Default; /* Post - Processing */
      Packet.platform_used                  = (float)platform;

      Packet.data_quality                   = Default; /* Post - Processing */;
      Packet.collection_subject_id          = Default; /* Post - Processing */;
      Packet.imu_position                   = Default; /* Post - Processing */;
      Packet.collection_env                 = Default; /* Post - Processing */;
      Packet.multiple_speed_flag            = Default; /* Post - Processing */;
      Packet.speed                          = Default; /* Post - Processing */;
      Packet.mult_incline_flag              = Default; /* Post - Processing */;
      Packet.incline_pct                    = Default; /* Post - Processing */;

      Packet.time_scale                     = (float)TIME_RESOLUTION; 
      Packet.sample_rate_flag               = Default; /* Post - Processing */;
      Packet.sample_rate_ave                = Default; /* Post - Processing */;
      Packet.sample_rate_std                = Default; /* Post - Processing */;
      Packet.number_of_samples              = Default; /* Post - Processing */;
      Packet.number_of_elements_per_sample  = 10.0f; /* Post - Processing */;
      Packet.orientation_PO                 = (float)PITCH_O;
      Packet.orientation_PRC                = (float)PITCH_ROT_CONV;
      Packet.orientation_RRC                = (float)ROLL_ROT_CONV;
      Packet.orientation_ZR                 = (float)ROLL_ZREF;
      
      break;
      
    case 2 :
      break;
      
    default :
      break;
  } /* End switch(DATA_PACKET_VERSION) */

  LOG_DATA( &Packet, sizeof(META_PACKET_TYPE) );
  
} /* End Meta_LogOut */


/*************************************************
** FUNCTION: Data_LogOut
** VARIABLES:
**    [I ]  CONTROL_TYPE      *p_control
**    [I ]  SENSOR_STATE_TYPE *p_sensor_state
**    [I ]  GAPA_STATE_TYPE   *p_gapa_state
**    [I ]  WISE_STATE_TYPE   *p_wise_state
** RETURN:
**    NONE
** DESCRIPTION:
**    This function will pack and write the specified
**    data to the data log file (if logging to file is 
**    enabled).
*/
void Data_LogOut( CONTROL_TYPE       *p_control,
                  SENSOR_STATE_TYPE  *p_sensor_state,
                  GAPA_STATE_TYPE    *p_gapa_state,
                  WISE_STATE_TYPE    *p_wise_state)
{
  float Packet[10];
  
  Packet[0] = (float)p_control->timestamp;
  Packet[1] = (float)p_sensor_state->accel.val[0];
  Packet[2] = (float)p_sensor_state->accel.val[1];
  Packet[3] = (float)p_sensor_state->accel.val[2];
  Packet[4] = (float)p_sensor_state->gyro.val[0];
  Packet[5] = (float)p_sensor_state->gyro.val[1];
  Packet[6] = (float)p_sensor_state->gyro.val[2];
  Packet[7] = (float)TO_DEG(p_sensor_state->yaw.val[0]);
  Packet[8] = (float)TO_DEG(p_sensor_state->pitch.val[0]);
  Packet[9] = (float)TO_DEG(p_sensor_state->roll.val[0]);
  
  LOG_DATA( &Packet, 10*sizeof(float) );
  
} /* End Data_LogOut() */


/*************************************************
** FUNCTION: Debug_LogOut
** VARIABLES:
**    [I ]  CONTROL_TYPE      *p_control
**    [I ]  SENSOR_STATE_TYPE *p_sensor_state
**    [I ]  WISE_STATE_TYPE   *p_wise_state
** RETURN:
**    NONE
** DESCRIPTION:
**    This function just prints a standard string
**    to the log_port serial port.
**    It prints the rpy as well as the timestamp and
**    and estimate of the sample rate
*/
void Debug_LogOut( CONTROL_TYPE       *p_control,
                   SENSOR_STATE_TYPE  *p_sensor_state,
                   GAPA_STATE_TYPE    *p_gapa_state,
                   WISE_STATE_TYPE    *p_wise_state)
{
  char LogBuffer[MAX_LINE_LEN];
  char tmpBuffer[MAX_LINE_LEN];

  switch ( p_control->output_mode )
  {
    case 1:    /* IMU Values */
//      FltToStr( p_gapa_state->nu_norm.val[0], 4, tmpBuffer );
//      strcat( LogBuffer, tmpBuffer );
//  UART_PORT.print((float)TO_DEG(p_sensor_state->yaw.val[0]));
//  UART_PORT.print(',');
//  UART_PORT.println((float)TO_DEG(p_sensor_state->pitch.val[0]));
//  UART_PORT.print(',');
//  UART_PORT.println((float)TO_DEG(p_sensor_state->roll.val[0]));
  

      UART_PORT.print(p_sensor_state->accel.val[0]*0.0001,3);
      UART_PORT.print(',');
      UART_PORT.print(p_sensor_state->accel.val[1]*0.0001,3);
      UART_PORT.print(',');
      UART_PORT.print(p_sensor_state->accel.val[2]*0.0001,3);
      UART_PORT.print(';');
      UART_PORT.print(p_sensor_state->gyro.val[0]*0.0001,3);
      UART_PORT.print(',');
      UART_PORT.print(p_sensor_state->gyro.val[1]*0.0001,3);
      UART_PORT.print(',');
      UART_PORT.print(p_sensor_state->gyro.val[2]*0.0001,3);
      UART_PORT.print(';');
      UART_PORT.println(p_gapa_state->nu_norm.val[0],3);

//  Packet[8] = (float)TO_DEG(p_sensor_state->pitch.val[0]);
//  Packet[9] = (float)TO_DEG(p_sensor_state->roll.val[0]);

// print roll and pitch vals for debugging
      
//      UART_PORT.print((float)TO_DEG(p_sensor_state->pitch.val[0]), 2);
//      UART_PORT.print(',');
//      UART_PORT.println((float)TO_DEG(p_sensor_state->roll.val[0]), 2);
      break;
    
    default:
      break;
  }

  //LOG_INFO(LogBuffer);
} /* End Debug_LogOut */


/*************************************************
** FUNCTION: Cal_LogOut
** VARIABLES:
**    [I ]  SENSOR_STATE_TYPE *p_sensor_state
**    [I ]  CALIBRATION_TYPE  *p_calibration
** RETURN:
**    NONE
** DESCRIPTION:
**    This function just prints a standard string
**    to the log_port serial port.
**    It is designed to assist in the calibration
**    of the sensor
*/
void Cal_LogOut( CONTROL_TYPE      *p_control,
                 SENSOR_STATE_TYPE *p_sensor_state,
                 CALIBRATION_TYPE  *p_calibration )
{
  char LogBuffer[MAX_LINE_LEN];
  char tmpBuffer[MAX_LINE_LEN];


  sprintf( LogBuffer, "TIME: %09lu", p_control->timestamp );

  strcat( LogBuffer, ", DT: " );
  FltToStr( p_control->G_Dt, 4, tmpBuffer );
  strcat( LogBuffer, tmpBuffer );

  strcat( LogBuffer, ", SR: " );
  FltToStr( 1/p_control->G_Dt, 4, tmpBuffer );
  strcat( LogBuffer, tmpBuffer );

  switch ( p_control->calibration_prms.output_mode )
  {
    case 0:
      strcat( LogBuffer, ", accel (min/ave/max): " );

      strcat( LogBuffer, "[a1](" );
      FltToStr( p_calibration->accel_min[0], 4, tmpBuffer );
      strcat( LogBuffer, tmpBuffer );

      strcat( LogBuffer, "/" );
      FltToStr( p_calibration->accel_total[0]/p_calibration->N, 4, tmpBuffer );
      strcat( LogBuffer, tmpBuffer );

      strcat( LogBuffer, "/" );
      FltToStr( p_calibration->accel_max[0], 4, tmpBuffer );
      strcat( LogBuffer, tmpBuffer );
      strcat( LogBuffer, "), " );


      strcat( LogBuffer, "[a2](" );
      FltToStr( p_calibration->accel_min[1], 4, tmpBuffer );
      strcat( LogBuffer, tmpBuffer );

      strcat( LogBuffer, "/" );
      FltToStr( p_calibration->accel_total[1]/p_calibration->N, 4, tmpBuffer );
      strcat( LogBuffer, tmpBuffer );

      strcat( LogBuffer, "/" );
      FltToStr( p_calibration->accel_max[1], 4, tmpBuffer );
      strcat( LogBuffer, tmpBuffer );
      strcat( LogBuffer, "), " );


      strcat( LogBuffer, "[a3](" );
      FltToStr( p_calibration->accel_min[2], 4, tmpBuffer) ;
      strcat( LogBuffer, tmpBuffer );

      strcat( LogBuffer, "/" );
      FltToStr( p_calibration->accel_total[2]/p_calibration->N, 4, tmpBuffer);
      strcat( LogBuffer, tmpBuffer );

      strcat( LogBuffer, "/" );
      FltToStr( p_calibration->accel_max[2], 4, tmpBuffer );
      strcat( LogBuffer, tmpBuffer );
      strcat( LogBuffer, ")" );
      break;

    case 1:
      strcat( LogBuffer, ", gyro (ave/current): " );

      strcat( LogBuffer, "[g1](" );
      FltToStr( p_calibration->gyro_total[0]/p_calibration->N, 4, tmpBuffer );
      strcat( LogBuffer, tmpBuffer );

      strcat( LogBuffer, "/" );
      FltToStr( p_sensor_state->gyro.val[0], 4, tmpBuffer );
      strcat( LogBuffer, tmpBuffer );
      strcat( LogBuffer, "), " );

      strcat( LogBuffer, "[g2](" );
      FltToStr( p_calibration->gyro_total[1]/p_calibration->N, 4, tmpBuffer);
      strcat( LogBuffer, tmpBuffer );

      strcat( LogBuffer, "/" );
      FltToStr( p_sensor_state->gyro.val[1], 4, tmpBuffer);
      strcat( LogBuffer, tmpBuffer );
      strcat( LogBuffer, "), " );

      strcat( LogBuffer, "[g3](" );
      FltToStr( p_calibration->gyro_total[2]/p_calibration->N, 4, tmpBuffer );
      strcat( LogBuffer, tmpBuffer );

      strcat( LogBuffer, "/" );
      FltToStr( p_sensor_state->gyro.val[2], 4, tmpBuffer );
      strcat( LogBuffer, tmpBuffer );
      strcat( LogBuffer, ")" );
      break;
  }

  LOG_INFO(LogBuffer);
} /* End Cal_LogOut */




/*************************************************
** FUNCTION: FltToStr
** VARIABLES:
**    [I ]  float value
**    [I ]  int   precision
**    [IO]  char *StrBuffer
** RETURN:
**    NONE
** DESCRIPTION:
**    This function converts a floating point
**    number into a string. This is needed to
**    support logging floats in Arduino.
*/
void FltToStr( float value,
               int   precision,
               char *StrBuffer )
{
  StrBuffer[0] = '\0';
  switch ( precision )
  {
    case 0:
      sprintf(StrBuffer, "%d", (int)value);
      break;
    case 1:
      sprintf(StrBuffer, "%d.%01d", (int)value, ABS((int)(value*10)%10) );
      break;
    case 2:
      sprintf(StrBuffer, "%d.%02d", (int)value, ABS((int)(value*100)%100) );
      break;
    case 3:
      sprintf(StrBuffer, "%d.%03d", (int)value, ABS((int)(value*1000)%1000) );
      break;
    case 4:
      sprintf(StrBuffer, "%d.%04d", (int)value, ABS((int)(value*10000)%10000) );
      break;
    case 5:
      sprintf(StrBuffer, "%d.%05d", (int)value, ABS((int)(value*100000)%100000) );
      break;
    case 6:
      sprintf(StrBuffer, "%d.%06d", (int)value, ABS((int)(value*1000000)%1000000) );
      break;
    case 7:
      sprintf(StrBuffer, "%d.%07d", (int)value, ABS((int)(value*10000000)%10000000) );
      break;
    case 8:
      sprintf(StrBuffer, "%d.%08d", (int)value, ABS((int)(value*100000000)%100000000) );
      break;
    case 9:
      sprintf(StrBuffer, "%d.%09d", (int)value, ABS((int)(value*1000000000)%1000000000) );
      break;
    case 10:
      sprintf(StrBuffer, "%d.%010d", (int)value, ABS((int)(value*10000000000)%10000000000) );
      break;
    case 11:
      sprintf(StrBuffer, "%d.%011d", (int)value, ABS((int)(value*100000000000)%100000000000) );
      break;
    case 12:
      sprintf(StrBuffer, "%d.%012d", (int)value, ABS((int)(value*1000000000000)%1000000000000) );
      break;
  }
}

/*************************************************
** FUNCTION: LogToFile
** VARIABLES:
**    [I ]  CONTROL_TYPE         *p_control
**    [I ]  OUTPUT_LOG_FILE_TYPE *log_file,
**    [I ]  char*                 message
** RETURN:
**    void
** DESCRIPTION:
**    This is a helper function.
**    It is used for logging to a file (SD or local).
**    This function will add data to the output buffers
**    and (when the buffer has reached the defined length)
**    write the buffer to the appropriate output file.
*/
void LogToFile( CONTROL_TYPE         *p_control,
                OUTPUT_LOG_FILE_TYPE *log_file,
                char*                 msg  )
{
  long int size_bytes;
  
  /* If logging to file is disabled,
  ** send to default out (wither uart or stdout)
  ** Only works with txt logging */
  if( log_file->enabled==FALSE )
  {
    if( log_file->type==0 ) /* type 0:txt */
    {
      LOG_INFO_DEFAULT( msg );
    }
    return;
  }

  /* Add message to output buffer */
  if( log_file->type==0 ) /* type 0:txt */
  {
    log_file->LogBufferLen += strlen( msg );
    strcat( log_file->LogBuffer, msg );
  }
  else
  {
    memcpy( &log_file->LogBuffer[log_file->LogBufferLen], msg, log_file->size );
    log_file->LogBufferLen += log_file->size;
  }

  /* If buffer has reached designated size ...*/
  if( log_file->LogBufferLen > MAX_LOG_BUFFER_STORE )
  {
    /* If the filehandle is valid ...
    ** NOTE : File is kept open during execution
    **        First open is in common_init */
    if( log_file->LogFile_fh!=NULL )
    {
      /* Get current file size */
      //size_bytes = 0; /* Force 1 file */
      size_bytes = FILE_SIZE_BYTES(log_file->LogFile_fh);

      /* If the filesize is larger than the designated
      ** max, close file and open next index */
      if( size_bytes>MAX_OUTPUT_FILE_SIZE )
      {
        if( log_file->LogFileIdx>LOG_FILE_MAX_IDX )
        {
          FILE_CLOSE( log_file->LogFile_fh );
          log_file->enabled = FALSE;
        }
        else
        {
          FILE_CLOSE( log_file->LogFile_fh );
          GetNextLogFileName( p_control, log_file );

          if( log_file->type==0 ) /* type 0:txt */
          {
            log_file->LogFile_fh = FILE_OPEN_WRITE( log_file->LogFileName );
          }
          else /* type 1:bin */
          {
            log_file->LogFile_fh = FILE_OPEN_WRITE_B( log_file->LogFileName );
          }
        }
      }
      if( log_file->LogFile_fh==NULL )
      {
        log_file->enabled        = FALSE;
        #if( EXE_MODE==0 ) /* 0 : IMU Mode */
          p_control->SDCardPresent = FALSE;
        #endif
      }
      else
      {
        if( log_file->type==0 ) /* type 0:txt */
        {
          FILE_PRINT_TO_FILE( log_file->LogFile_fh, log_file->LogBuffer );
          FILE_FLUSH( log_file->LogFile_fh );
        }
        else /* type 1:bin */
        {
          size_bytes = FILE_WRITE_TO_FILE( (log_file->LogBuffer), 1, log_file->LogBufferLen, log_file->LogFile_fh );
          FILE_FLUSH( log_file->LogFile_fh );
        }
        log_file->LogBuffer[0] = '\0';
        log_file->LogBufferLen = 0;
      }
    }
    else
    {
      log_file->enabled          = FALSE;
      #if( EXE_MODE==0 ) /* 0 : IMU Mode */
        p_control->SDCardPresent = FALSE;
      #endif
    } /* End if log_file->LogFile_fh!=NULL */
  } /* End if log_file->LogBufferLen > MAX_LOG_BUFFER_STORE */
} /* End LogToFile() */



/*************************************************
** FUNCTION: GetNextLogFileName
** VARIABLES:
**    [I ]  CONTROL_TYPE      *p_control
** RETURN:
**    void
** DESCRIPTION:
**    This is a helper function.
**    It is used for logging to an SD card.
**    This function creates a filename which does not
**    exist on the card, to which we will log our data.
*/
void GetNextLogFileName( CONTROL_TYPE          *p_control,
                         OUTPUT_LOG_FILE_TYPE  *log_file )
{
  int  i;

  for( i=log_file->LogFileIdx; i<LOG_FILE_MAX_IDX; i++ )
  {
    /* Construct a file with PREFIX[Index].SUFFIX */
    sprintf( log_file->LogFileName, "%s%i.%s", log_file->file_prefix, i, log_file->file_suffix );
    LOG_INFO( " > Trying File %s", log_file->LogFileName );

    /* If the file name doesn't exist, return it */
    //if( !SD.exists(log_file->LogFileName) )
    if( ! FILE_EXISTS_FLAG(log_file->LogFileName) )
    {
      LOG_INFO( " > File %s Available", log_file->LogFileName );
      log_file->LogFileIdx = i + 1;
      break;
    }
  }
} /* End GetNextLogF */

