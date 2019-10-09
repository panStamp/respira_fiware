/**
 * Copyright (c) 2019 panStamp <contact@panstamp.com>
 * 
 * This file is part of the RESPIRA project.
 * 
 * panStamp  is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * any later version.
 * 
 * panStamp is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with panStamp; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301
 * USA
 * 
 * Author: Daniel Berenguer
 * Creation date: Sep 5 2019
 */

#ifndef _RESPIRA_TB600_H
#define _RESPIRA_RB600_H

/**
 * Return codes
 */
#define RESPIRA_TB600_OK               0
#define RESPIRA_TB600_ERROR_NOREPLY    1
#define RESPIRA_TB600_ERROR_BADREPLY   2

class RESPIRA_TB600
{
  private:
    /**
     * Serial port
     */
    HardwareSerial *serPort;

    /**
     * Raw instant gas concentration in ppb
     */
    float rawConcentration;
    
    /**
     * Filtered instant gas concentration in ppb
     */
    float filtConcentration;

    /**
     * Average concentration in ppb
     */
    uint32_t avgConcentration;

    /**
     * Number of samples for the calculation of the average
     */
    uint16_t avgSamples;

    /**
     * Minimum gas concentration detected
     */
    float minConcentration;

    /**
     * Zero offset
     */
    float zeroOffset;

    /**
     * Sensor calibration parameters
     */
    float no2Factor, no2Offset;

    /**
     * Enable zero calibration
     */
    bool enZeroCalib;

    /**
     * setAnswerMode
     * 
     * Put device in Question-Answer mode
     */
    inline void setAnswerMode(void)
    {
      const uint8_t cmd[] = {0xFF, 0x01, 0x78, 0x41, 0x00, 0x00, 0x00, 0x00, 0x46};

      serPort->write(cmd, sizeof(cmd));
    }

    /**
     * setActiveMode
     * 
     * Put device in Active mode
     */
    inline void setActiveMode(void)
    {
      const uint8_t cmd[] = {0xFF, 0x01, 0x78, 0x40, 0x00, 0x00, 0x00, 0x47};

      serPort->write(cmd, sizeof(cmd));
    }

  public:
    /**
     * Class constructor
     *
     * @param port : serial port
     */
    inline RESPIRA_TB600(HardwareSerial *port)
    {
      serPort = port;
      filtConcentration = 0;
      rawConcentration = 0;
      minConcentration = 0;
      zeroOffset = 0;
      resetAvg();
      enZeroCalib = false;
      no2Factor = 1;
      no2Offset = 0;
    }

    /**
     * begin
     * 
     * Initialize sensor board
     * 
     * @return return code
     */
    inline uint8_t begin(void)
    {
      serPort->begin(9600);

      Serial.println("TB600 : Entering Question and Answer mode");
      setAnswerMode();

      return RESPIRA_TB600_OK;
    }

    /**
     * read
     * 
     * Request reading and read response from sensor
     * 
     * @param temp Current temperature for compensation
     *
     * @return Return code
     */
    inline uint8_t read(float temp=20.0)
    {
      const uint8_t cmd[] = {0xFF, 0x01, 0x86, 0x00, 0x00, 0x00, 0x00, 0x00, 0x79};

      // Flush serial port
      serPort->flush();
      while(serPort->available() > 0)
        char t = serPort->read();

      // Transmit query
      serPort->write(cmd, sizeof(cmd));
      delay(50);

      // Wait for response from sensor board. Timeout = 5000 msec
      uint16_t timeout = 5000;
      
      // Read response from sensor
      uint8_t len=0, buffer[9];
      while (len < sizeof(buffer))
      {        
        while ((serPort->available()))
          buffer[len++] = serPort->read();

        if (timeout-- == 0)
          return RESPIRA_TB600_ERROR_NOREPLY;

        delay(1);
      }

      if ((buffer[0] != 0xFF) || (buffer[1] != 0x86))
        return RESPIRA_TB600_ERROR_BADREPLY;
      
      uint16_t conc = (buffer[6] << 8) | buffer[7];

      // Raw (non filtered) concentration
      rawConcentration = (float) conc;
      
      // Compensate for temperature
      tempCompensation(temp);

      // Update minimum concentration
      if ((minConcentration == 0) || (minConcentration > rawConcentration))
        minConcentration = rawConcentration;
        
      // Factor/offset correction
      filtConcentration = rawConcentration * no2Factor + no2Offset;
      
      // Zero callibration
      if (enZeroCalib)
        filtConcentration -= zeroOffset;

      // Skip negative values
      if (filtConcentration < 0)
        filtConcentration = 0;

      Serial.print("TB600 : Raw NO2 = "); Serial.print(rawConcentration); Serial.print(" ppb - ");
      Serial.print("TB600 : Filtered NO2 = "); Serial.print(filtConcentration); Serial.print(" ppb - ");
      Serial.print("Min NO2 = "); Serial.print(minConcentration); Serial.println(" ppb");

      // Update average
      avgConcentration += filtConcentration;
      avgSamples++;

      return RESPIRA_TB600_OK;
    }

    /**
     * tempCompensation
     * 
     * Compensate reading for temperature
     * 
     * @param temp Temperature in ºC
     */
    inline void tempCompensation(float temp)
    {
     // Calculate sensitivity at 20 ºC
     float sens = 0.002 * sq(20) - 0.2233 * 20 -19.862;
     // Get raw reading
     float raw = rawConcentration / sens;
     // Calculate sensitivity at temp
     sens = 0.002 * sq(temp) - 0.2233 * temp -19.862;
     // Get concentration at temp
     rawConcentration = raw * sens;
    }

    /**
     * getPpb
     * 
     * Get last filtered reading in ppb's
     * 
     * @return Last reading in ppb
     */
    inline float getPpb(void)
    {
     return filtConcentration;
    }

    /**
     * getAvgPpb
     * 
     * Get average concentration in ppb's
     * 
     * @return Average in ppb
     */
    inline float getAvgPpb(void)
    {
     if (avgSamples == 0)
       return 0.0;
       
     return (float)(avgConcentration / avgSamples);
    }

    /**
     * getAvgUgM3
     * 
     * Get average concentration in μg/m3
     * 
     * @return Average in μg/m3
     */
    inline float getAvgUgM3(void)
    {        
     return 1.8814 * getAvgPpb();
    }

    /**
     * resetAvg
     * 
     * Reset average variables
     */
    inline void resetAvg(void)
    {
     avgConcentration = 0;
     avgSamples = 0;
    }

    /**
     * zeroCalibrate
     * 
     * Apply zero offset calibration
     */
    inline void zeroCalibrate(void)
    {
      Serial.println("TB600 : Updating zero offset");
      zeroOffset = minConcentration;
      minConcentration = 0;
    }
    
    /**
     * setCalibParams
     * 
     * Set calibration parameters
     * 
     * @param factor Correction factor
     * @param offset Correction offset
     */
    inline void setCalibParams(float factor, float offset)
    {      
      no2Factor = factor;
      no2Offset = offset;
      
      Serial.print("TB600 : calibration factor: ");
      Serial.print(no2Factor);
      Serial.print(" - offset : ");
      Serial.println(no2Offset);
    }
    
    /**
     * enableZeroCalib
     * 
     * Enable or disable zero calibration
     * 
     * @param enabled Enabling flag
     */
    inline void enableZeroCalib(bool enabled)
    {      
      enZeroCalib = enabled;
      
      Serial.print("TB600 : Zero calibration enabled: ");
      Serial.println(enZeroCalib);
    }
    
    /**
     * getCaqi
     * 
     * Calculate CAQI EU-supported Air Quality Index
     * 
     * @return CAQI index
     */
    inline uint16_t getCaqi(void)
    {
      uint16_t conc = (uint16_t) getAvgUgM3();
      uint16_t caqi = 0;
      
      if (conc <= 100)
        caqi = conc / 2;
      else if (conc <= 200)
        caqi = map(conc, 100, 200, 50, 75);
      else if (conc <= 400)
        caqi = map(conc, 200, 400, 75, 100);
      else
        caqi = conc / 4;

      return caqi;
    }
};
#endif

