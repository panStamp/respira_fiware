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
# Date: Sep 18 2019
#########################################################################

from config.config import AfConfig
from afexception import AfException
from afhttpclient import AfHttpClient

import json


class Afiware(object):
    """
    FIWARE UL interface
    """

    CREATE_SERVICE_GROUP = True

    def create_service_group_observation(self):
        """
        Create service group on FIWARE CB
        """

        ## Post request
        try:
            url = AfConfig.FIWARE_SERVGROUP_URL
            params = {}
            headers = {"Content-Type": "application/json", "fiware-service": AfConfig.FIWARE_SERVICE, "fiware-servicepath": "/" + AfConfig.FIWARE_ENTITY_OBSERVATION}

            # Declare datamodels
            attributes = []

            for key, value in AfConfig.FIWARE_DATAMODEL_OBSERVATION.items():
                if key in AfConfig.FIWARE_DATAMODEL_STRINGS:
                    attr = {"object_id": key, "name": value, "type": "String"}
                else:
                    attr = {"object_id": key, "name": value, "type": "Number"}

                attributes.append(attr)
            
            payload = {"services": [{"apikey": AfConfig.FIWARE_APIKEY, "protocol": ["IoTA-UL"], "cbroker": "http://orion:1026", "entity_type": AfConfig.FIWARE_ENTITY, "resource": "/iot/d", "attributes": attributes}]}            
            
            client = AfHttpClient(headers, url, params, json.dumps(payload))
            client.post()

        except:
            raise AfException("Unable to create service group. Probably because it already exists")


    def create_service_group(self, api_key, entity_type, data_model):
        """
        Create service group on FIWARE CB

        @param api_key: FIWARE API Key
        @param entity_type: Entity type (FIWARE_ENTITY_OBSERVATION or FIWARE_ENTITY_POLLUTION)
        @param data_model: List of correspondances between UL and NGSI nomenclatures
        """

        ## Post request
        try:
            url = AfConfig.FIWARE_SERVGROUP_URL
            params = {}
            headers = {"Content-Type": "application/json", "fiware-service": AfConfig.FIWARE_SERVICE, "fiware-servicepath": "/" + entity_type}

            # Declare datamodels
            attributes = []

            for key, value in data_model.items():
                if key in AfConfig.FIWARE_DATAMODEL_STRINGS:
                    attr = {"object_id": key, "name": value, "type": "String"}
                else:
                    attr = {"object_id": key, "name": value, "type": "Number"}

                attributes.append(attr)
            
            payload = {"services": [{"apikey": api_key, "protocol": ["IoTA-UL"], "cbroker": "http://orion:1026", "entity_type": entity_type, "resource": "/iot/d", "attributes": attributes}]}            
            
            client = AfHttpClient(headers, url, params, json.dumps(payload))
            client.post()

        except:
            raise AfException("Unable to create service group. Probably because it already exists")


    def __init__(self, api_key, entity, timestamp, payload):
        '''
        Constructor

        @param api_key: FIWARe API Key
        @param entity: Entity name
        @param timestamp: timestamp of data creation    
        @param payload: UltraLight payload to be transmitted to FIWARE IoT agent
        '''        
        # Create service group the first time an object is created
        if Afiware.CREATE_SERVICE_GROUP:
            Afiware.CREATE_SERVICE_GROUP = False
            try:
                self.create_service_group(AfConfig.FIWARE_APIKEY_OBSERVATION, AfConfig.FIWARE_ENTITY_OBSERVATION, AfConfig.FIWARE_DATAMODEL_OBSERVATION)
            except AfException as ex:
                ex.show()

            try:
                self.create_service_group(AfConfig.FIWARE_APIKEY_POLLUTION, AfConfig.FIWARE_ENTITY_POLLUTION, AfConfig.FIWARE_DATAMODEL_POLLUTION)
            except AfException as ex:
                ex.show()

        # Send UL packet
        try:
            url = AfConfig.FIWARE_UL_URL
            params = {"k" : api_key, "i": entity, "t": timestamp.strftime("%Y-%m-%dT%H:%M:%SZ"), "getCmd": 1}
            headers = {"Content-Type": "text/plain"}
            client = AfHttpClient(headers, url, params, payload)
            client.post()

        except:
            raise AfException("Unable to post UL packet to FIWARE IoT agent")
