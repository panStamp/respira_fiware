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

from config.config import RespConfig
from respexception import RespException
from resphttpclient import RespHttpClient

import json


class RespFiware(object):
    """
    FIWARE UL interface
    """

    CREATE_SERVICE_GROUP = True


    def list_service_groups(self):
        """
        List all service groups under the service and service path configured in config.py
        """

        ## Post request
        try:
            url = RespConfig.FIWARE_SERVGROUP_URL
            params = {}
            headers = {"fiware-service": RespConfig.FIWARE_SERVICE, "fiware-servicepath": RespConfig.FIWARE_SERVICE_PATH}
           
            client = RespHttpClient(headers, url, params, "")
            result = client.get()

            return json.dumps(result, indent=4, sort_keys=True)

        except:
            raise RespException("Unable to query service groups")


    def create_service_group(self, api_key):
        """
        Create service group on FIWARE CB

        @param api_key: FIWARE API Key
        """

        ## Post request
        try:
            url = RespConfig.FIWARE_SERVGROUP_URL
            params = {}
            headers = {"Content-Type": "application/json", "fiware-service": RespConfig.FIWARE_SERVICE, "fiware-servicepath": RespConfig.FIWARE_SERVICE_PATH}

            # Declare datamodels
            attributes = []

            for key, value in RespConfig.FIWARE_DATAMODEL.items():
                if key in RespConfig.FIWARE_DATAMODEL_STRINGS:
                    attr = {"object_id": key, "name": value, "type": "String"}
                else:
                    attr = {"object_id": key, "name": value, "type": "Number"}

                attributes.append(attr)
            
            config = {"name": "config", "type": "String", "value": "0|1|0|0|1|0|1|0|1|0|1|0"}
            attributes.append(config)
            payload = {"services": [{"apikey": api_key, "protocol": ["IoTA-UL"], "cbroker": "http://orion:1026", "entity_type": RespConfig.FIWARE_ENTITY_TYPE, "resource": "/iot/d", "attributes": attributes}]}           
           
            client = RespHttpClient(headers, url, params, json.dumps(payload))
            client.post()

            print("Service group successfully created")

        except:
            raise RespException("Unable to create service group. Probably because it already exists")


    def delete_service_group(self, api_key):
        """
        Delete service group from FIWARE CB

        @param api_key: FIWARE API Key
        """

        ## Post request
        try:
            url = RespConfig.FIWARE_SERVGROUP_URL
            params = {"resource": "/iot/d", "apikey": api_key}
            headers = {"fiware-service": RespConfig.FIWARE_SERVICE, "fiware-servicepath": RespConfig.FIWARE_SERVICE_PATH}
            
            client = RespHttpClient(headers, url, params, "")
            result = client.delete()

            print(result)
            print("Service group successfully deleted")

        except:
            raise RespException("Unable to delete service group")


    def set_config(self, device_id, config_str):
        """
        Set config string for device

        @param device_id: device ID
        @param config_str: configuration string
        """        
        url = RespConfig.FIWARE_ENTITIES_URL + RespConfig.FIWARE_SERVICE_PATH + ":" + device_id + "/attrs"
        params = {}
        headers = {"Content-Type": "application/json", "fiware-service": RespConfig.FIWARE_SERVICE, "fiware-servicepath": RespConfig.FIWARE_SERVICE_PATH}

        # Build default HTTP body
        body = {"config": {"value": config_str, "type": "String"}}
        
        try: 
            client = RespHttpClient(headers, url, params, json.dumps(body))
            client.patch()
        except:
            raise RespException("Unable to update calibration setttings for device " + device_id)

        print("Calibration settings successfully updated for device " + device_id)


    def reset_calibration(self, device_id):
        """
        Reset calibration settings for device

        @param device_id: device ID
        """        
        ## Post request
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
        ## Post request
        try:
            url = RespConfig.FIWARE_ENTITIES_URL + RespConfig.FIWARE_SERVICE_PATH + ":" + device_id + "/attrs"
            params = {}
            headers = {"fiware-service": RespConfig.FIWARE_SERVICE, "fiware-servicepath": RespConfig.FIWARE_SERVICE_PATH}

            # Query current config settings
            client = RespHttpClient(headers, url + "/config", params, "")
            result = client.get()

            # Check response from CB           
            if "value" not in result:
                raise RespException("Reply from CB incorrectly formatted")

            # Read config
            config = result["value"].split("|")

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
            raise RespException("Unable to retrieve calibration setttings for dewvice " + device_id + " and polluant " + polluant)


    def set_zero_calibration(self, device_id, sensor, enable):
        """
        Set automatic zero calibration flag for device and sensor

        @param device_id: device ID
        @param sensor: sensor name (no2, pm)
        @param enable: enable (True) or disable (False) zero calibration
        """        
        ## Post request
        try:
            url = RespConfig.FIWARE_ENTITIES_URL + RespConfig.FIWARE_SERVICE_PATH + ":" + device_id + "/attrs"
            params = {}
            headers = {"fiware-service": RespConfig.FIWARE_SERVICE, "fiware-servicepath": RespConfig.FIWARE_SERVICE_PATH}

            # Query current config settings
            client = RespHttpClient(headers, url + "/config", params, "")
            result = client.get()

            # Check response from CB           
            if "value" not in result:
                raise RespException("Reply from CB incorrectly formatted")

            # Read config
            config = result["value"].split("|")

            # Modify zero calibration flag
            if sensor == "no2":
                config[0] = enable
            elif sensor == "pm":
                config[3] = enable

            # Rebuild config string
            config_str = "|".join(config)

            try:
                self.set_config(device_id, config_str)
            except:
                raise

        except:
            raise RespException("Unable to retrieve calibration setttings for dewvice " + device_id + " and polluant " + polluant)


    def enable_zero_calibration(self, device_id, sensor):
        """
        Enable automatic zero calibration flag for device and sensor

        @param device_id: device ID
        @param sensor: sensor name (no2, pm)
        """        
        try:
            set_zero_calibration(device_id, sensor, True)
        except:
            raise


    def disable_zero_calibration(self, device_id, sensor):
        """
        Disable automatic zero calibration flag for device and sensor

        @param device_id: device ID
        @param sensor: sensor name (no2, pm)
        """        
        try:
            set_zero_calibration(device_id, sensor, False)
        except:
            raise


    def list_devices(self):
        """
        List devices and their values
        """        
        ## Post request
        try:
            url = RespConfig.FIWARE_ENTITIES_URL
            params = {}

            headers = {"fiware-service": RespConfig.FIWARE_SERVICE, "fiware-servicepath": RespConfig.FIWARE_SERVICE_PATH}

            # Query current config settings
            client = RespHttpClient(headers, url, params, "")
            result = client.get()
            return json.dumps(result, indent=4, sort_keys=True)
        except:
            raise RespException("Unable to retrieve list of devices")


    def read_device(self, device_id, show_values):
        """
        Read device values

        @param device_id: device ID
        @param show_values: show only values
        """        
        ## Post request
        try:
            url = RespConfig.FIWARE_ENTITIES_URL + "/" + RespConfig.FIWARE_ENTITY_TYPE + ":" + device_id + "/attrs"

            if show_values:
                params = {"options": "keyValues"}
            else:
                params = {}

            headers = {"fiware-service": RespConfig.FIWARE_SERVICE, "fiware-servicepath": RespConfig.FIWARE_SERVICE_PATH}

            # Query current config settings
            client = RespHttpClient(headers, url, params, "")
            result = client.get()
            return json.dumps(result, indent=4, sort_keys=True)
        except:
            raise RespException("Unable to retrieve values for device " + device_id)


    def delete_device(self, device_id):
        """
        Delete device

        @param device_id: device ID
        """        
        ## Post request
        try:
            url = RespConfig.FIWARE_ENTITIES_URL + "/" + RespConfig.FIWARE_ENTITY_TYPE + ":" + device_id
            params = {}

            headers = {"fiware-service": RespConfig.FIWARE_SERVICE, "fiware-servicepath": RespConfig.FIWARE_SERVICE_PATH}

            # Query current config settings
            client = RespHttpClient(headers, url, params, "")
            client.delete()

            print("Device successfully deleted")
        except:
            raise RespException("Unable to delete device " + device_id)

        
    def __init__(self):
        '''
        Constructor
        '''        
        pass
