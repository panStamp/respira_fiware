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
 * Creation date: Oct 5 2019
 */

/**
 * Enable watchdog
 */
//#define WATCHDOG_ENABLED  1

/**
 * FIWARE settings
 */
const char FIWARE_SERVER[] = "63.35.250.27";

// NGSI setings
const uint16_t FIWARE_QRY_PORT = 1026; // NGSI entity query port
const char FIWARE_SERVICE[] = "openiot";
const char FIWARE_SERVICE_PATH[] = "/RESPIRA_T3";

// UltraLight setings
const uint16_t FIWARE_UL_PORT = 7896;  // UltraLight port
const char FIWARE_APIKEY[] = "si95g7noxpmah9cbx9ggoe36va";

/**
 * Sampling interval in msec
 */
const uint32_t SAMPLING_INTERVAL = 20000; // 20 sec

/**
 * Transmission interval in msec
 */
const uint32_t TX_INTERVAL = 3600000; // 1 hour

/**
 * Zero calibration interval for the NO2 sensor
 */
const uint32_t ZERO_CALIB_INTERVAL = 10 * 24 * 3600000; // 10 days

