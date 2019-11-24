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
 * Creation date: Nov 23 2019
 */

#include <ESP8266WiFi.h>
#include <DNSServer.h>
#include <ESP8266WebServer.h>
#include <WiFiManager.h>         //https://github.com/tzapu/WiFiManager

#include "config.h"
#include "fiware.h"
#include "SparkFun_Si7021_Breakout_Library.h"

// LED pin
#define LED  2

// Wifi managerapp
WiFiManager wifiManager;
const char wmPassword[] = "respira";

// Device MAC address
char deviceMac[16];

// Description string
char deviceId[32];

// FIWARE object
FIWARE fiware(FIWARE_SERVER, FIWARE_UL_PORT, FIWARE_APIKEY, APP_NAME);

// Sensor object
Weather si7021;

// Time of last transmission in msec
uint32_t lastTxTime = 0;


/**
 * transmit
 *
 * Build UL string and transmit to FIWARE IoT agent
 *
 * @return true in case of sucess
 */
bool transmit(void)
{
  char txBuf[64];
 
  // Read sensor
  float temperature = si7021.getTemp();
  float humidity = si7021.getRH();
      
  // Preparing UL frame
  sprintf(txBuf, "t|%.2f|h|%.2f",
    temperature,
    humidity
  );  

  Serial.println(txBuf);

  return fiware.send(deviceId, txBuf); 
}

/**
 * Main setup function
 */
void setup()
{
  // Let the power supply stabilize
  delay(3000);
  
  // Setup UART
  Serial.begin(115200);
  Serial.println();
  
  // Config LED pin
  pinMode(LED, OUTPUT);
  digitalWrite(LED, HIGH);
 
  // Get MAC
  WiFi.begin();
  uint8_t mac[6];
  WiFi.macAddress(mac);
  sprintf(deviceMac, "%02X%02X%02X%02X%02X%02X", mac[0], mac[1], mac[2], mac[3], mac[4], mac[5]);

  // Device ID
  sprintf(deviceId, "%s_%s", APP_NAME, deviceMac);

  Serial.print("Device ID:"); Serial.println(deviceId);
  Serial.print("API Key: "); Serial.println(FIWARE_APIKEY);

  digitalWrite(LED, LOW);

  // WiFi Manager timeout
  wifiManager.setConfigPortalTimeout(300);

  // WiFi Manager autoconnect
  if (!wifiManager.autoConnect(deviceId))
  {
    Serial.println("failed to connect and hit timeout");
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

  // Initialize sensor
  si7021.begin();

  digitalWrite(LED, HIGH);
}

/**
 * Endless loop
 */
void loop()
{
  if (!lastTxTime || ((millis() - lastTxTime) >= TX_INTERVAL))
  {
    digitalWrite(LED, LOW);
  
    Serial.println("Transmitting UL frame");
    if (transmit())
    {
      Serial.println("OK");
      lastTxTime = millis();
    }
     
    digitalWrite(LED, HIGH);
  }
}
