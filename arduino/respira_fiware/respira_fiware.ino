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
#include "sensor.h"

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
const char FIWARE_APIKEY[] = "5g4d8yt2d37gh12schq6l5z47x";
FIWARE fiware(FIWARE_SERVER, FIWARE_PORT, FIWARE_APIKEY);

// RESPIRA sensor set
RESPIRA_SENSOR sensor;

// Tx interval in msec
const uint32_t TX_INTERVAL = 60000;

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
  
  sprintf(txBuf, "t|%.2f#h|%.2f#no2|%.2f#mpm1|%.2f#mpm2|%.2f#mpm4|%.2f#mpm10|%.2f#npm0|%.2f#npm1|%.2f#npm2|%.2f#npm4|%.2f#npm10|%.2f#avgs|%.2f",
    sensor.getTemperature(),
    sensor.getHumidity(),
    sensor.getNO2(),
    sensor.getMassPM1(),
    sensor.getMassPM2(),
    sensor.getMassPM4(),
    sensor.getMassPM10(),
    sensor.getNumPM0(),
    sensor.getNumPM1(),
    sensor.getNumPM2(),
    sensor.getNumPM4(),
    sensor.getNumPM10(),
    sensor.getAvgSize()
  );

  Serial.println(txBuf);

  digitalWrite(LED, HIGH);
  bool ret = fiware.send(deviceId, txBuf);
  digitalWrite(LED, LOW);

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

  // Initialize sensor set
  sensor.begin();

  digitalWrite(LED, LOW);

}

/**
 * Endless loop
 */
void loop()
{
  if ((millis() - lastTxTime) >= TX_INTERVAL)
  {
    Serial.println("Reading SPS30");
    if (sensor.read())
    {
      Serial.println("Transmitting");
      if (transmit())
      {
        Serial.println("OK");
        lastTxTime = millis();
      }
    }
  }
  
  #ifdef WATCHDOG_ENABLED
  // Reset WDT (feed watchdog)
  timerWrite(timer, 0);
  #endif

  delay(5000);
}

