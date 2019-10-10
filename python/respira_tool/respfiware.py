#########################################################################
# Copyright (c) 2019 panStamp <contact@panstamp.com>
# 
# This file is part of the RESPIRA-FIWARE project.
# 
# panStamp  is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# any later version.
# 
# panStamp is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with panStamp; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 
# USA
#
# Author: Daniel Berenguer
# Date: Oct 1 2019
#########################################################################

from config import RespConfig
from respexception import RespException
from resphttpclient import RespHttpClient

import json
import importlib


class RespFiware(object):
    """
    FIWARE UL interface
    """

    def set_service_path(self, service_path):
        """
        Set new service path
        """
        RespConfig.FIWARE_SERVICE_PATH = service_path
        RespConfig.save_config()


    def read_service_path(self):
        """
        Read service path
        """
        return RespConfig.FIWARE_SERVICE_PATH


    def get_config(self, device_id):
        """
        Get configuration string from device

        @param device_id: device ID
        """        
        try:
            url = RespConfig.FIWARE_ENTITIES_URL + "/" + RespConfig.FIWARE_ENTITY_TYPE + ":" + device_id + "/attrs/config/value"
            params = {}
            headers = {"fiware-service": RespConfig.FIWARE_SERVICE, "fiware-servicepath": RespConfig.FIWARE_SERVICE_PATH}

            # Query current config settings
            client = RespHttpClient(headers, url, params, "")
            return client.get()

        except:
            raise RespException("Unable to retrieve config string for device " + device_id)


    def set_config(self, device_id, config_str):
        """
        Set config string for device

        @param device_id: device ID
        @param config_str: configuration string
        """        
        url = RespConfig.FIWARE_ENTITIES_URL + "/" + RespConfig.FIWARE_ENTITY_TYPE + ":" + device_id + "/attrs"
        params = {}
        headers = {"Content-Type": "application/json", "fiware-service": RespConfig.FIWARE_SERVICE, "fiware-servicepath": RespConfig.FIWARE_SERVICE_PATH}

        # Build default HTTP body
        body = {"config": {"value": config_str, "type": "String"}}
        
        try: 
            client = RespHttpClient(headers, url, params, json.dumps(body))
            client.patch()
        except:
            raise RespException("Unable to update calibration setttings for device " + device_id)


    def reset_calibration(self, device_id):
        """
        Reset calibration settings for device

        @param device_id: device ID
        """        
        try:
            config_str = "0|1|0|0|1|0|1|0|1|0|1|0"
            self.set_config(device_id, config_str)
        except:
            raise


    def calibrate(self, device_id, polluant, factor, offset):
        """
        Set calibration settings for device and polluant

        @param device_id: device ID
        @param polluant: polluant name (no2, pm1.0, pm2.5, pm4.0, pm10)
        @param factor: calibration factor
        @param offset: calibration offset
        """        
        try:           
            # Read config
            result = self.get_config(device_id)
            config = result.split("|")

            # Save zero calibration flags
            zero_no2 = config[0]
            zero_pm = config[3]

            # And drop zero calibration flags
            config.pop(0)
            config.pop(2)

            # Get index of polluant
            try:
                index = RespConfig.POLLUANTS.index(polluant)
            except ValueError:
                raise RespException(polluant + " not supported")

            # Update factor and offset in config list
            config[index * 2] = str(factor)
            config[index * 2 + 1] = str(offset)

            # Append zero calibration flags
            config.insert(0, zero_no2)
            config.insert(2, zero_pm)

            # Rebuild config string
            config_str = "|".join(config)

            try:
                self.set_config(device_id, config_str)
            except:
                raise

        except:
            raise RespException("Unable to retrieve calibration setttings for device " + device_id + " and polltuant " + polluant)


    def print_calibration(self, device_id):
        """
        Read calibration settings

        @param device_id: device ID
        """        
        try:
            result = self.get_config(device_id)
        except:
            raise
        try:
            config = result.split("|")

            zero_calib_en = "disabled"
            if config[0] == '1':
                zero_calib_en = "enabled"

            print("NO2 automatic zero-calibration: " + zero_calib_en)
            print("NO2 correction factor (gain): " + str(config[1]))
            print("NO2 correction offset: " + str(config[2]))

            zero_calib_en = "enabled"
            if config[3] == 0:
                zero_calib_en = "disabled"

            print("PM sensor automatic zero-calibration: " + zero_calib_en)
            print("PM1.0 correction factor (gain): " + str(config[4]))
            print("PM1.0 correction offset: " + str(config[5]))
            print("PM2.5 correction factor (gain): " + str(config[6]))
            print("PM2.5 correction offset: " + str(config[7]))
            print("PM4.0 correction factor (gain): " + str(config[8]))
            print("PM4.0 correction offset: " + str(config[9]))
            print("PM10 correction factor (gain): " + str(config[10]))
            print("PM10 correction offset: " + str(config[11]))

        except:
            raise RespException("Unable to retrieve config values for device " + device_id)


    def set_zero_calibration(self, device_id, sensor, enable):
        """
        Set automatic zero calibration flag for device and sensor

        @param device_id: device ID
        @param sensor: sensor name (no2, pm)
        @param enable: enable (True) or disable (False) zero calibration
        """        
        ## Post request
        try:
            # Read config
            result = self.get_config(device_id)
        except:
            raise
        try:
            flag = '0'
            if enable:
                flag = '1'

            config = result.split("|")

            # Modify zero calibration flag
            if sensor == "no2":
                config[0] = flag
            elif sensor == "pm":
                config[3] = flag

            # Rebuild config string
            config_str = "|".join(config)

            try:
                self.set_config(device_id, config_str)
            except:
                raise

        except:
            raise RespException("Unable to write automatic zero-calibration for device " + device_id + " and sensor " + sensor)


    def enable_zero_calibration(self, device_id, sensor):
        """
        Enable automatic zero calibration flag for device and sensor

        @param device_id: device ID
        @param sensor: sensor name (no2, pm)
        """        
        try:
            self.set_zero_calibration(device_id, sensor, True)
        except:
            raise


    def disable_zero_calibration(self, device_id, sensor):
        """
        Disable automatic zero calibration flag for device and sensor

        @param device_id: device ID
        @param sensor: sensor name (no2, pm)
        """        
        try:
            self.set_zero_calibration(device_id, sensor, False)
        except:
            raise


    def __init__(self):
        '''
        Constructor
        '''        
        RespConfig.load_config()
