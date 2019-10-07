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
 * Creation date: Jul 24 2019
 */

#include <WiFi.h>
#include <esp_system.h>
#include <DNSServer.h>
#include <WebServer.h>
#include <WiFiManager.h>         // https://github.com/tzapu/WiFiManager

#include "config.h"
#include "fiware.h"
#include "respira_sps30.h"
#include "respira_tb600.h"
#include "respira_si7021.h"

/**
 * Watchdog
 */
#ifdef WATCHDOG_ENABLED
const uint32_t WATCHDOG_DELAY = 30000000; // in usec
const int loopTimeCtl = 0;
hw_timer_t *timer = NULL;
#endif

// LED pin
#define LED  2

// Wifi manager
WiFiManager wifiManager;
const char wmPassword[] = "respira";

// Device MAC address
char deviceMac[16];

// Description string
char deviceId[32];

// Application name
const char appName[] = "RESPIRA";

// FIWARE object
FIWARE fiware(FIWARE_SERVER, FIWARE_UL_PORT, FIWARE_APIKEY, FIWARE_QRY_PORT, FIWARE_SERVICE, FIWARE_SERVICE_PATH, appName);

// RESPIRA sensor set
RESPIRA_SPS30 sps30;
RESPIRA_TB600 no2Sensor(&Serial2);
RESPIRA_SI7021 si7021;

// Time of last sample in msec
uint32_t lastSampleTime = 0;

// Zero calibration for the NO2 sensor
const uint32_t ZERO_CALIB_LOOPS = ZERO_CALIB_INTERVAL - TX_INTERVAL;
uint16_t zeroCalibLoops = 0;

// Time of last transmission in msec
uint32_t lastTxTime = 0;

// First reading after startup
bool firstReading = true;

// force transmission
bool transmitNow = false;

/**
 * Restart board
 */
void restart(void)
{
  // Restart ESP32
  ESP.restart();  
}

/**
 * readSettings
 * 
 * Read settings received from CB
 * 
 * @param settings Settings received in string format
 * 
 * @return True in case of command successfully processed
 */
bool readSettings(char *settings)
{
  char *ptr1 = settings, *ptr2;
  uint8_t numParam = 0;
  float params[12];

  // Parse config string
  while((ptr2 = strchr(ptr1, '|')) != NULL)
  {
    if (numParam == sizeof(params))
      return false;
      
    ptr2[0] = 0;      
    params[numParam++] = atof(ptr1);
    ptr1 = ptr2 + 1;                
  }

  // Last paramter
  params[numParam++] = atof(ptr1);

  // Check number of parameters and update settings 
  if (numParam == (sizeof(params)/sizeof(float)))
  {
    Serial.println("Updating config settings");
    
    no2Sensor.enableZeroCalib(params[0] > 0);
    no2Sensor.setCalibParams(params[1], params[2]);
    sps30.enableZeroCalib(params[3] > 0);
    sps30.setCalibParams(params[4], params[5], params[6], params[7], params[8], params[9], params[10], params[11]);

    return true;
  }
}

/**
 * transmit
 *
 * Build UL string and transmit to FIWARE IoT agent
 *
 * @return true in case of sucess
 */
bool transmit(void)
{
  char txBuf[256];

  // No2 concentration in μg/m3
  float no2Conc = (float) no2Sensor.getAvgUgM3();
  // CAQI index related to NO2 concentration
  uint16_t caqiNo2 = no2Sensor.getCaqi();
  
  // Temperature in ºC
  float temperature = si7021.getAvgTemperature();
  // Relative humidity
  float humidity = si7021.getAvgHumidity();  

  // Particulate matter
  float pm1 = sps30.getAvgPM1();
  float pm2 = sps30.getAvgPM2();
  float pm4 = sps30.getAvgPM4();
  float pm10 = sps30.getAvgPM10();
  float typSize = sps30.getTypSize();
  // CAQI index related to PM concentration
  uint16_t caqiPm = sps30.getCaqi();

  // Global CAQI index
  uint16_t caqi = caqiPm;
  if (caqiNo2 > caqiPm)
    caqi = caqiNo2;

  // Preparing UL frame
  sprintf(txBuf, "t|%.2f|h|%.2f|no2|%.2f|pm1|%.2f|pm2|%.2f|pm4|%.2f|pm10|%.2f|typs|%.2f|q|%d",
    temperature,
    humidity,
    no2Conc,
    pm1,
    pm2,
    pm4,
    pm10,
    typSize,
    caqi
  );  

  Serial.println(txBuf);

  bool ret = fiware.send(deviceId, txBuf); 

  // OK received from server?
  if (ret)
  {   
    // Reset averages
    no2Sensor.resetAvg();
    si7021.resetAvg();
    sps30.resetAvg();
  }

  return ret;
}

/**
 * Main setup function
 */
void setup()
{
  // Setup UART
  Serial.begin(115200);
  Serial.println();
  
  // Config LED pin
  pinMode(LED, OUTPUT);
  digitalWrite(LED, LOW);

  // Get MAC
  WiFi.begin();
  uint8_t mac[6];
  WiFi.macAddress(mac);
  sprintf(deviceMac, "%02X%02X%02X%02X%02X%02X", mac[0], mac[1], mac[2], mac[3], mac[4], mac[5]);

  // Device ID
  sprintf(deviceId, "%s_%s", appName, deviceMac);

  Serial.print("Device ID:"); Serial.println(deviceId);
  Serial.print("API Key: "); Serial.println(FIWARE_APIKEY);

  digitalWrite(LED, HIGH);
   
  if (!wifiManager.autoConnect(deviceId))
  {
    Serial.println("failed to connect and hit timeout");
    //reset and try again, or maybe put it to deep sleep
    ESP.restart();
    delay(1000);
  }
  else
  {
    Serial.println("");
    Serial.print("MAC address: ");
    Serial.println(deviceMac);
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());
  }

  #ifdef WATCHDOG_ENABLED
  // Watchdog timer
  timer = timerBegin(0, 80, true); //timer 0, div 80
  timerAttachInterrupt(timer, &restart, true);
  timerAlarmWrite(timer, WATCHDOG_DELAY, false); //set time in us
  timerAlarmEnable(timer); //enable interrupt
  #endif

  // Initialize sensors
  sps30.begin();
  no2Sensor.begin();
  si7021.begin();

  digitalWrite(LED, LOW);

  lastSampleTime = millis();
}

/**
 * Endless loop
 */
void loop()
{
  if ((millis() - lastSampleTime) >= SAMPLING_INTERVAL)
  {
    digitalWrite(LED, HIGH);
    Serial.println("Reading SPS30");
    if (sps30.read() == RESPIRA_SPS30_OK)
    {
      Serial.println("Reading NO2 sensor");
      if (no2Sensor.read() == RESPIRA_TB600_OK)
      {
        Serial.println("Reading SI7021 sensor");
        si7021.read();
        lastSampleTime = millis();
      }
    }
    digitalWrite(LED, LOW);

    if (firstReading)
    {
      // Force transmission
      firstReading = false;
      transmitNow = true;
    }
  }

  if (((millis() - lastTxTime) >= TX_INTERVAL) || transmitNow)
  {
    digitalWrite(LED, HIGH);

    if (transmitNow)
      transmitNow = false;

    // Query calibration settings
    char settings[FIWARE_SERVER_RESPONSE_MAXLEN];
    settings[0] = 0;  // Default contents

    Serial.println("Retrieving config settings from FIWARE CB");

    if (fiware.querySettings(settings, deviceId))
      readSettings(settings);

    Serial.println("Transmitting UL frame");
    if (transmit())
    {
      Serial.println("OK");
      lastTxTime = millis();

      // Zero calibrate?
      if (++zeroCalibLoops == ZERO_CALIB_LOOPS)
      {
        zeroCalibLoops = 0;
        no2Sensor.zeroCalibrate();
      }
    }
    digitalWrite(LED, LOW);
  }
  
  #ifdef WATCHDOG_ENABLED
  // Reset WDT (feed watchdog)
  timerWrite(timer, 0);
  #endif

  delay(1000);
}

