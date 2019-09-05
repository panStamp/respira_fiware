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

#define RESPIRA_TB600_ERROR_CODE  -1

class RESPIRA_TB600
{
  private:
    /**
     * Serial port
     */
    HardwareSerial *serPort;

    /**
     * Gas concentration in ppb
     */
    uint16_t concentration;
  
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
      concentration = 0;
    }

    /**
     * begin
     * 
     * Initialize sensor board
     * 
     * @return error code
     */
    inline uint8_t begin(void)
    {
      serPort->begin(9600);
      setAnswerMode();
    }

    /**
     * read
     * 
     * Request reading and read response from sensor
     *
     * @return Gas concentration in ppb
     */
    inline float read(void)
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
        {
          buffer[len] = serPort->read();
          Serial.print(buffer[len], HEX);
          Serial.print(" ");
          len++;
        }

        if (timeout-- == 0)
          return RESPIRA_TB600_ERROR_CODE;

        delay(1);
      }
      Serial.println("");

      concentration = (buffer[6] << 8) | buffer[7];

      Serial.print("NO2 concentration : ");
      Serial.print(concentration);
      Serial.println(" ppb");
    }

    /**
     * getPpb
     * 
     * Get last reading in ppb's
     * 
     * @return Last reading in ppb
     */
     uint16_t getPpb(void)
     {
       return concentration;
     }
};
#endif

