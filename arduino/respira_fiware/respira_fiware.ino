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
#include <WiFiManager.h>         //https://github.com/tzapu/WiFiManager

#include "fiware.h"
#include "respira_sps30.h"
#include "respira_tb600.h"
#include "respira_si7021.h"

/**
 * Watchdog
 */
//#define WATCHDOG_ENABLED  1
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

/**
 * FIWARE settings
 */
const char FIWARE_SERVER[] = "54.154.169.181";
const uint16_t FIWARE_PORT = 7896;
const char FIWARE_APIKEY[] = "4jggokgpepnvsb2uv4s40d59ab"; //"5g4d8yt2d37gh12schq6l5z47x";
FIWARE fiware(FIWARE_SERVER, FIWARE_PORT, FIWARE_APIKEY);

// RESPIRA sensor set
RESPIRA_SPS30 sps30;
RESPIRA_TB600 no2Sensor(&Serial2);
RESPIRA_SI7021 si7021;

// Sampling interval in msec
const uint32_t SAMPLING_INTERVAL = 20000; // 20 sec

// Time of last sample in msec
uint32_t lastSampleTime = 0;

// Tx interval in msec
const uint32_t TX_INTERVAL = 3600000; // 1 hour

// Zero calibration interval
const uint32_t ZERO_CALIB_INTERVAL = 10 * 24 * 3600000; // 10 days
const uint32_t ZERO_CALIB_LOOPS = ZERO_CALIB_INTERVAL - TX_INTERVAL;
uint16_t zeroCalibLoops = 0;

// Time of last transmission in msec
uint32_t lastTxTime = 0;

/**
 * Restart board
 */
void restart(void)
{
  // Restart ESP32
  ESP.restart();  
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

  // Preparing UL frame
  sprintf(txBuf, "t|%.2f#h|%.2f#no2|%.2f#pm1|%.2f#pm2|%.2f#pm4|%.2f#pm10|%.2f#typs|%.2f",
    temperature,
    humidity,
    no2Conc,
    pm1,
    pm2,
    pm4,
    pm10,
    typSize
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
  }

  if ((millis() - lastTxTime) >= TX_INTERVAL)
  {
    digitalWrite(LED, HIGH);
    Serial.println("Transmitting");
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

