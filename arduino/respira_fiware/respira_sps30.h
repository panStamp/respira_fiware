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

/**
 * Return codes
 */
#define RESPIRA_SPS30_OK               0
#define RESPIRA_SPS30_ERROR_NOREPLY    1
#define RESPIRA_SPS30_ERROR_BADREPLY   2
#define RESPIRA_SPS30_ERROR_NOTFOUND   3
#define RESPIRA_SPS30_ERROR_NOTRESET   4
#define RESPIRA_SPS30_ERROR_NOCLEAN    5
#define RESPIRA_SPS30_ERROR_NOSTART    6

class RESPIRA_SPS30
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

    /**
     * Average concentration of particles
     */
    float avgConcPm1, avgConcPm2, avgConcPm4, avgConcPm10, avgSize;

    /**
     * Number of samples for the calculation of the averages
     */
    uint16_t avgSamples;

    /**
     * Minimum concentration values
     */
    float minPm1, minPm2, minPm4, minPm10;


    /**
     * Zero offset
     */
    float zeroOffsetPm1, zeroOffsetPm2, zeroOffsetPm4, zeroOffsetPm10;
    
    /**
     * Sensor calibration parameters
     */
    float pm1Factor, pm1Offset, pm2Factor, pm2Offset, pm4Factor, pm4Offset, pm10Factor, pm10Offset;
    
    /**
     * Enable zero calibration
     */
    bool enZeroCalib;

  public:
    /**
     * Class constructor
     */
    inline RESPIRA_SPS30(void)
    {
      resetAvg();

      minPm1 = 0;
      minPm2 = 0;
      minPm4 = 0;
      minPm10 = 0;
      
      enZeroCalib = false;
      zeroOffsetPm1 = 0;
      zeroOffsetPm2 = 0;
      zeroOffsetPm4 = 0;
      zeroOffsetPm10 = 0;
      
      pm1Factor = 1;
      pm1Offset = 0;
      pm2Factor = 1;
      pm2Offset = 0;
      pm4Factor = 1;
      pm4Offset = 0;
      pm10Factor = 1;
      pm10Offset = 0;
    }
    
    /**
     * begin
     * 
     * Initialize sensor
     * 
     * @return Return code
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
        Serial.println("Could not probe / connect with SPS30.");
        return RESPIRA_SPS30_ERROR_NOTFOUND;
      }
      else
        Serial.println("Detected SPS30.");

      // reset SPS30 connection
      if (sps30.reset() == false)
      {
        Serial.println("Could not reset SPS30.");
        return RESPIRA_SPS30_ERROR_NOTRESET;
      }

      uint32_t interval;
      uint8_t ret;
  
      // Get autoclean interval
      if (sps30.GetAutoCleanInt(&interval) == ERR_OK)
      {
        Serial.print("SPS30 : Current Auto Clean interval: ");
        Serial.print(interval);
        Serial.println(" seconds");
      }
      else
      {
        Serial.println("Could not get clean interval.");
        return RESPIRA_SPS30_ERROR_NOCLEAN;
      }
       
      // Default autoclean interval (~ 1 week)
      interval = 604800;
      if (sps30.SetAutoCleanInt(interval) == ERR_OK)
      {
        Serial.print("SPS30 : Auto Clean interval now set : ");
        Serial.print(interval);
        Serial.println(" seconds");
      }
      else
      {
        Serial.println("SPS30 : Could not set clean interval.");
        return RESPIRA_SPS30_ERROR_NOCLEAN;
      }
          
      // Start measurement
      if (sps30.start() == true)
        Serial.println("SPS30 : Measurement started");
      else
      {
        Serial.println("SPS30 : Could NOT start measurement from SPS30");
       return RESPIRA_SPS30_ERROR_NOSTART;
      }

      // Clean now
      if (sps30.clean() == true)
        Serial.println("SPS30 : Fan-cleaning manually started");
      else
      {
        Serial.println("SPS30 : Could NOT manually start fan-cleaning");
        return RESPIRA_SPS30_ERROR_NOCLEAN;
      }

      return RESPIRA_SPS30_OK;
    }

    /*
     * read
     * 
     * Read sensors
     * 
     * @return Return code
     */
    inline uint8_t read(void)
    {
      if (sps30.GetValues(&sps30Values) != ERR_OK)
      {
        Serial.println("SPS30 : Error reading values from SPS30 sensor");
        return RESPIRA_SPS30_ERROR_NOREPLY;
      }

      Serial.print("SPS30 : PM1.0 = "); Serial.print(getMassPM1()); Serial.print(" ug/m3 - ");
      Serial.print("PM2.5 = "); Serial.print(getMassPM2()); Serial.print(" ug/m3 - ");
      Serial.print("PM4.0 = "); Serial.print(getMassPM4()); Serial.print(" ug/m3 - ");
      Serial.print("PM10 = "); Serial.print(getMassPM10()); Serial.print(" ug/m3 - ");
      Serial.print("Avg size  = "); Serial.print(getTypSize()); Serial.println(" um");

      float filtPM1 = getMassPM1();
      float filtPM2 = getMassPM2();
      float filtPM4 = getMassPM4();
      float filtPM10 = getMassPM10();

      // Update minimum concentrations
      if ((minPm1 == 0) || (minPm1 > filtPM1))
        minPm1 = filtPM1;
      if ((minPm2 == 0) || (minPm2 > filtPM2))
        minPm2 = filtPM2;
      if ((minPm4 == 0) || (minPm4 > filtPM4))
        minPm4 = filtPM4;
      if ((minPm10 == 0) || (minPm10 > filtPM10))
        minPm10 = filtPM10;

      // Run factor/offset corrections
      filtPM1 = filtPM1 * pm1Factor + pm1Offset;
      filtPM2 = filtPM2 * pm2Factor + pm2Offset;
      filtPM4 = filtPM4 * pm4Factor + pm4Offset;
      filtPM10 = filtPM10 * pm10Factor + pm10Offset;
      
      // Run zero calibration
      if (enZeroCalib)
      {
        filtPM1 -= zeroOffsetPm1;
        filtPM2 -= zeroOffsetPm2;
        filtPM4 -= zeroOffsetPm4;
        filtPM10 -= zeroOffsetPm10;
      }

      // Update averages
      avgConcPm1 += filtPM1;
      avgConcPm2 += filtPM2;
      avgConcPm4 += filtPM4;
      avgConcPm10 += filtPM10;     
      avgSize += getTypSize();
      avgSamples++;

      return RESPIRA_SPS30_OK;
    }
        
    /*
     * getMassPM1
     * 
     * Get mass concentration of the PM1.0 particles from SPS30 sensor
     * 
     * @return mass concentration of the PM1.0 particles in μg/m3
     */
    inline float getMassPM1(void)
    {
      return sps30Values.MassPM1;
    }

    /*
     * getMassPM2
     * 
     * Get mass concentration of the PM2.5 particles from SPS30 sensor
     * 
     * @return mass concentration of the PM2.5 particles in μg/m3
     */
    inline float getMassPM2(void)
    {
      return sps30Values.MassPM2;
    }

    /*
     * getMassPM4
     * 
     * Get mass concentration of the PM4.0 particles from SPS30 sensor
     * 
     * @return mass concentration of the PM4.0 particles in μg/m3
     */
    inline float getMassPM4(void)
    {
      return sps30Values.MassPM4;
    }

    /*
     * getMassPM10
     * 
     * Get mass concentration of the PM10 particles from SPS30 sensor
     * 
     * @return mass concentration of the PM10 particles in μg/m3
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
     * getTypSize
     * 
     * Get typical size of the particles measured from SPS30 sensor
     * 
     * @return typical size of particles in μm
     */
    inline float getTypSize(void)
    {
      return sps30Values.PartSize;
    }

    /**
     * getAvgPM1
     * 
     * Get average concentration of PM1.0
     * 
     * @return Average concentration in μg/m3
     */
    inline float getAvgPM1(void)
    {
      if (avgSamples == 0)
        return 0.0;
         
      return avgConcPm1 / avgSamples;
    }

    /**
     * getAvgPM2
     * 
     * Get average concentration of PM2.5
     * 
     * @return Average concentration in μg/m3
     */
    inline float getAvgPM2(void)
    {
      if (avgSamples == 0)
        return 0.0;
       
      return avgConcPm2 / avgSamples;
    }

    /**
     * getAvgPM4
     * 
     * Get average concentration of PM4.0
     * 
     * @return Average concentration in μg/m3
     */
    inline float getAvgPM4(void)
    {
      if (avgSamples == 0)
        return 0.0;
       
      return avgConcPm4 / avgSamples;
    }

    /**
     * getAvgPM10
     * 
     * Get average concentration of PM10
     * 
     * @return Average concentration in μg/m3
     */
    inline float getAvgPM10(void)
    {
      if (avgSamples == 0)
        return 0.0;
       
      return avgConcPm10 / avgSamples;
    }

    /**
     * getAvgSize
     * 
     * Get average size of particles
     * 
     * @return Average size in μM
     */
    inline float getAvgSize(void)
    {
      if (avgSamples == 0)
        return 0.0;
       
      return avgSize / avgSamples;
    }
     
    /**
     * resetAvg
     * 
     * Reset average variables
     */
    inline void resetAvg(void)
    {
      avgConcPm1 = 0;
      avgConcPm2 = 0;
      avgConcPm4 = 0;
      avgConcPm10 = 0;
      avgSize = 0;
      avgSamples = 0;
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

      Serial.print("SPS30 : Zero calibration enabled: ");
      Serial.println(enZeroCalib);
    }

    /**
     * zeroCalibrate
     * 
     * Apply zero offset calibration
     */
    inline void zeroCalibrate(void)
    {
      Serial.println("SPS30 : Updating zero offsets");
      zeroOffsetPm1 = minPm1;
      zeroOffsetPm2 = minPm2;
      zeroOffsetPm4 = minPm4;
      zeroOffsetPm10 = minPm10;    

      minPm1 = 0;
      minPm2 = 0;
      minPm4 = 0;
      minPm10 = 0;
    }
    
    /**
     * setCalibParams
     * 
     * Set calibration parameters
     * 
     * @param pm1F PM1.0 correction factor
     * @param pm1O PM1.0 correction offset
     * @param pm2F PM2.5 correction factor
     * @param pm2O PM2.5 correction offset
     * @param pm4F PM4.0 correction factor
     * @param pm4O PM4.0 correction offset
     * @param pm10F PM10 correction factor
     * @param pm10O PM10 correction offset
     */
    inline void setCalibParams(float pm1F, float pm1O, float pm2F, float pm2O, float pm4F, float pm4O, float pm10F, float pm10O)
    {     
      pm1Factor = pm1F;
      pm1Offset = pm1O;
      pm2Factor = pm2F;
      pm2Offset = pm2O;
      pm4Factor = pm4F;
      pm4Offset = pm4O;
      pm10Factor = pm10F;
      pm10Offset = pm10O;

      Serial.print("TB600 : PM1.0 calibration factor: ");
      Serial.print(pm1Factor);
      Serial.print(" - offset : ");
      Serial.println(pm1Offset);
      Serial.print("TB600 : PM2.5 calibration factor: ");
      Serial.print(pm2Factor);
      Serial.print(" - offset : ");
      Serial.println(pm2Offset);
      Serial.print("TB600 : PM4.0 calibration factor: ");
      Serial.print(pm4Factor);
      Serial.print(" - offset : ");
      Serial.println(pm4Offset);
      Serial.print("TB600 : PM10 calibration factor: ");
      Serial.print(pm10Factor);
      Serial.print(" - offset : ");
      Serial.println(pm10Offset);
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
      uint16_t caqi2 = 0, caqi10 = 0;
      uint16_t pm2 = (uint16_t) avgConcPm2;
      uint16_t pm10 = (uint16_t) avgConcPm10;

      // Check PM2.5
      if (pm2 <= 30)
        caqi2 = map(pm2, 0, 30, 0, 50);
      else if (pm2 <= 55)
        caqi2 = map(pm2, 30, 55, 50, 75);
      else if (pm2 <= 110)
        caqi2 = map(pm2, 55, 110, 75, 100);
      else
        caqi2 = pm2 / 1.1;

      // Check PM10
      if (pm10 <= 50)
        caqi10 = pm10;
      else if (pm10 <= 90)
        caqi10 = map(pm10, 50, 90, 50, 75);
      else if (pm10 <= 180)
        caqi10 = map(pm10, 90, 180, 75, 100);
      else
        caqi10 = pm10 / 1.8;
        
      if (caqi2 > caqi10)
        return caqi2;

      return caqi10;
    }
};
#endif

