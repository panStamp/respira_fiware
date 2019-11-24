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

/**
 * Application name
 */
const char APP_NAME[] = "MYTHSENSOR";

/**
 * FIWARE settings
 */
const char FIWARE_SERVER[] = "calidadmedioambiental.org";

// UltraLight setings
const uint16_t FIWARE_UL_PORT = 80; // UltraLight port
const char FIWARE_APIKEY[] = "F0qS8OkPlh0fgwUCcXFnc8JLlu";

/**
 * Transmission interval in msec
 */
const uint32_t TX_INTERVAL = 300000; // 5 min

