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

#ifndef _FIWARE_H
#define _FIWARE_H

#include <stdarg.h>
#include <Arduino.h>
#include <ESP8266HTTPClient.h>

#define FIWARE_SERVER_STRING_MAXLEN    32


class FIWARE
{
  private:   
    /**
     * FIWARE server URL
     */
    char server[FIWARE_SERVER_STRING_MAXLEN];

    /**
     * FIWARE UltraLight API port
     */
    uint16_t ulPort;

    /**
     * Type of device
     */
    char deviceType[FIWARE_SERVER_STRING_MAXLEN];
    
    /**
     * Ultralight IoT agent API key
     */
    char apiKey[FIWARE_SERVER_STRING_MAXLEN];
        
  public:
    /**
     * Class constructor
     * 
     * @param fiwareServer FIWARE server URL or IP address
     * @param ulP Port for UltraLight API     
     * @param apiK UltraLight API key
     * @param devType Device type
     */
    inline FIWARE(const char *fiwareServer, const uint16_t ulP, const char *apiK, const char* devType)
    {
      strcpy(server, fiwareServer);
      ulPort = ulP;
      strcpy(apiKey, apiK);
      strcpy(deviceType, devType);
    }

    /**
     * send
     * 
     * Send attribute value
     * 
     * @param entity Entity name
     * @param attributes Attributes following UltraLight format (attr1|val1#attr1|val2...)
     * 
     * @return True in case of success. Return false otherwise
     */
    inline bool send(char *entity, char *attributes)
    {
      HTTPClient http;
      
      bool ret = false;
      
      // Make a HTTP request:
      char url[128];
      sprintf(url, "http://%s:%d/iot/d?k=%s&i=%s&getCmd=1", server, ulPort, apiKey, entity);
               
      http.begin(url);
      http.addHeader("Content-Type", "text/plain");
      int httpCode = http.POST(attributes);

      Serial.print("HTTP response: ");
      Serial.println(httpCode);
      
      if (httpCode == HTTP_CODE_OK)         
        ret = true;

      http.end();
      
      return ret;
    }
};
#endif
