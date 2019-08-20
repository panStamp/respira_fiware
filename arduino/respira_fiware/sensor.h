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
 * Creation date: Aug 6 2019
 */

#ifndef _RESPIRA_SENSOR_H
#define _RESPIRA_SENSOR_H

#include "sps30.h"  // Remember to disable INCLUDE_SOFTWARE_SERIAL in sps30.h

#define SP30_COMMS I2C_COMMS


class RESPIRA_SENSOR
{
  private:
    /**
     * SPS30 particle sensor object
     */
    SPS30 sps30;

    /**
     * SPS30 structure of values
     */
    struct sps_values sps30Values;

  public:
    /**
     * Class constructor
     */
    inline RESPIRA_SENSOR(void)
    {
    }

    /**
     * reset
     * 
     * Power-cycle sensors
     */
    inline void reset(void)
    {
    }
    
    /**
     * begin
     * 
     * Initialize sensors
     * 
     * @return error code
     */
    inline uint8_t begin(void)
    {
      // set driver debug level
      sps30.EnableDebugging(0);

      // Start communication with SPS30;
      if (sps30.begin(SP30_COMMS) == false)
      {
        Serial.println("could not initialize communication channel.");
        while(1) {}
      }
      
      // Check for SPS30 connection
      if (sps30.probe() == false)
      {
        Serial.println("could not probe / connect with SPS30.");
        while(1) {}
      }
      else
        Serial.println(F("Detected SPS30."));

      // reset SPS30 connection
      if (sps30.reset() == false)
      {
        Serial.println("Could not reset SPS30.");
        while(1) {}
      }

      uint32_t interval;
      uint8_t ret;
  
      // Get autoclean interval
      if (sps30.GetAutoCleanInt(&interval) == ERR_OK)
      {
        Serial.print(F("Current Auto Clean interval: "));
        Serial.print(interval);
        Serial.println(F(" seconds"));
      }
      else
      {
        Serial.println("Could not get clean interval.");
        while(1) {}
      }
       
      // Default autoclean interval (~ 1 week)
      interval = 604800;
      if (sps30.SetAutoCleanInt(interval) == ERR_OK)
      {
        Serial.print(F("Auto Clean interval now set : "));
        Serial.print(interval);
        Serial.println(F(" seconds"));
      }
      else
      {
        Serial.println("Could not set clean interval.");
        while(1) {}
      }
          
      // Start measurement
      if (sps30.start() == true)
        Serial.println(F("Measurement started"));
      else
      {
        Serial.println("Could NOT start measurement from SPS30");
        while(1) {}
      }

      // Clean now
      if (sps30.clean() == true)
        Serial.println(F("Fan-cleaning manually started"));
      else
        Serial.println(F("Could NOT manually start fan-cleaning"));
    }

    /*
     * read
     * 
     * Read sensors
     * 
     * @return True if function succees
     */
    inline bool read(void)
    {
      if (sps30.GetValues(&sps30Values) != ERR_OK)
      {
        Serial.println(F("Error reading values from SPS30 sensor"));
        return false;
      }

      return true;
    }
      
    /*
     * getTemperature
     * 
     * Get temeperature value from SI7021 sensor
     * 
     * @return temeperature in Celsius degrees
     */
    inline float getTemperature(void)
    {
      return 0.0;
    }

    /*
     * getHumidity
     * 
     * Get humidity value from SI7021 sensor
     * 
     * @return relative humidity
     */
    inline float getHumidity(void)
    {
      return 0.0;
    }

    /*
     * getNO2
     * 
     * Get NO2 concentration in ppm
     * 
     * @return NO2 concentration
     */
    inline float getNO2(void)
    {
      return 0.0;
    }
    
    /*
     * getMassPM1
     * 
     * Get mass of the PM1.0 particles from SPS30 sensor
     * 
     * @return mass of the PM1.0 particles in μg/m3
     */
    inline float getMassPM1(void)
    {
      return sps30Values.MassPM1;
    }

    /*
     * getMassPM2
     * 
     * Get mass of the PM2.5 particles from SPS30 sensor
     * 
     * @return mass of the PM2.5 particles in μg/m3
     */
    inline float getMassPM2(void)
    {
      return sps30Values.MassPM2;
    }

    /*
     * getMassPM4
     * 
     * Get mass of the PM4.0 particles from SPS30 sensor
     * 
     * @return mass of the PM4.0 particles in μg/m3
     */
    inline float getMassPM4(void)
    {
      return sps30Values.MassPM4;
    }

    /*
     * getMassPM10
     * 
     * Get mass of the PM10 particles from SPS30 sensor
     * 
     * @return mass of the PM10 particles in μg/m3
     */
    inline float getMassPM10(void)
    {
      return sps30Values.MassPM10;
    }

    /*
     * getNumPM0
     * 
     * Get concentration of the PM0.5 particles from SPS30 sensor
     * 
     * @return mass of the PM0.5 particles in #/cm3
     */
    inline float getNumPM0(void)
    {
      return sps30Values.NumPM0;
    }

    /*
     * getNumPM1
     * 
     * Get concentration of the PM1.0 particles from SPS30 sensor
     * 
     * @return mass of the PM1.0 particles in #/cm3
     */
    inline float getNumPM1(void)
    {
      return sps30Values.NumPM1;
    }

    /*
     * getNumPM2
     * 
     * Get concentration of the PM2.5 particles from SPS30 sensor
     * 
     * @return mass of the PM2.5 particles in #/cm3
     */
    inline float getNumPM2(void)
    {
      return sps30Values.NumPM2;
    }

    /*
     * getNumPM4
     * 
     * Get concentration of the PM4.0 particles from SPS30 sensor
     * 
     * @return mass of the PM4.0 particles in #/cm3
     */
    inline float getNumPM4(void)
    {
      return sps30Values.NumPM4;
    }

    /*
     * getNumPM10
     * 
     * Get concentration of the PM10 particles from SPS30 sensor
     * 
     * @return mass of the PM10 particles in #/cm3
     */
    inline float getNumPM10(void)
    {
      return sps30Values.NumPM10;
    }

    /*
     * getAvgSize
     * 
     * Get average size of the particles measured from SPS30 sensor
     * 
     * @return average size of particles in μm
     */
    inline float getAvgSize(void)
    {
      return sps30Values.PartSize;
    }
};
#endif

