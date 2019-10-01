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

    def create_service_group(self, api_key, entity_type, data_model):
        """
        Create service group on FIWARE CB

        @param api_key: FIWARE API Key
        @param entity_type: Entity type (FIWARE_ENTITY_OBSERVATION or FIWARE_ENTITY_POLLUTION)
        @param data_model: List of correspondances between UL and NGSI nomenclatures
        """

        ## Post request
        try:
            url = RespConfig.FIWARE_SERVGROUP_URL
            params = {}
            headers = {"Content-Type": "application/json", "fiware-service": RespConfig.FIWARE_SERVICE, "fiware-servicepath": "/" + entity_type}

            # Declare datamodels
            attributes = []

            for key, value in data_model.items():
                if key in RespConfig.FIWARE_DATAMODEL_STRINGS:
                    attr = {"object_id": key, "name": value, "type": "String"}
                else:
                    attr = {"object_id": key, "name": value, "type": "Number"}

                attributes.append(attr)
            
            payload = {"services": [{"apikey": api_key, "protocol": ["IoTA-UL"], "cbroker": "http://orion:1026", "entity_type": entity_type, "resource": "/iot/d", "attributes": attributes}]}            
            
            client = RespHttpClient(headers, url, params, json.dumps(payload))
            client.post()

        except:
            raise RespException("Unable to create service group. Probably because it already exists")


    def __init__(self):
        '''
        Constructor
        '''        
        pass
