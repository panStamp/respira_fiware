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
# Date: Dec 13 2019
#########################################################################

from config.config import FcbgConfig
from fcbgexception import FcbgException
from fcbghttpclient import FcbgHttpClient

import threading
import json


class FcbgUpdater(object):
    """
    FIWARE NGSI updater
    """

    def update_auth_token(self):
        """
        Update auth token from target server
        """
        url = FcbgConfig.FIWARE_AUTH_TOKEN_URL

        payload = "{\"auth\": {\"identity\": {\"methods\": [\"password\"],\"password\": {\"user\": {\"domain\": {\"name\": \""
        payload += FcbgConfig.FIWARE_TARGET_SERVICE + "\"},\"name\": \"" + FcbgConfig.FIWARE_TARGET_USER_NAME + "\",\"password\": \""
        payload += FcbgConfig.FIWARE_TARGET_USER_PASSWORD + "\"}}},\"scope\": {\"project\": {\"domain\": {\"name\": \""
        payload += FcbgConfig.FIWARE_TARGET_SERVICE + "\"},\"name\": \"" + FcbgConfig.FIWARE_TARGET_SERVICE_PATH + "\"}}}}"

        headers = {
            'Content-Type': "application/json"
            }

        
        threading.Timer(FcbgConfig.FIWARE_AUTH_TOKEN_INTERVAL, self.update_auth_token).start()

        try:
            client = FcbgHttpClient(headers, url, {}, payload)
            result = client.post()

            if result.status_code in [200, 201]:
                if "X-Subject-Token" in result.headers:
                    self.auth_token = result.headers["X-Subject-Token"]
            else:
                raise FcbgException("Unable to retrieve auth token from target server")
        except:
            raise


    def create(self, entity):
        """
        Create entity on target CB

        @param entity : Entity object
        """
        if "id" in entity and "type" in entity:
            entity_str = entity["type"] + ":" + entity["id"]

            # Create entity on target CB
            url = FcbgConfig.FIWARE_TARGET_URL
            headers = {
                "fiware-service": FcbgConfig.FIWARE_TARGET_SERVICE,
                "fiware-servicepath": FcbgConfig.FIWARE_TARGET_SERVICE_PATH,
                "Content-type" : "application/json",
                'X-Auth-Token': self.auth_token
                }

            try:
                client = FcbgHttpClient(headers, url, {}, json.dumps(entity))
                result = client.post()

                if result.status_code in [200, 201, 422]:
                    # Enter entity in memory
                    self.entities.append(entity_str)

                else:
                    raise FcbgException("Unable to create entity on target CB. Response: " + str(result.status_code) + ", Reason: " + result.reason)
            except:
                raise


    def update(self, entity):
        """
        Update entity on target CB

        @param entity : Entity object
        """
        if "id" in entity and "type" in entity:
            entity_str = entity["type"] + ":" + entity["id"]
            # Entity in memory?
            if entity_str in self.entities:
                # OK, update entity on target CB
                url = FcbgConfig.FIWARE_TARGET_URL + "/" + entity["id"] + "/attrs"
                headers = {
                    "fiware-service": FcbgConfig.FIWARE_TARGET_SERVICE,
                    "fiware-servicepath": FcbgConfig.FIWARE_TARGET_SERVICE_PATH,
                    "Content-type" : "application/json",
                    'X-Auth-Token': self.auth_token
                    }

                del entity["type"]
                del entity["id"]

                for field in entity:
                    if "metadata" in entity[field]:
                        del entity[field]["metadata"]

                try:
                    client = FcbgHttpClient(headers, url, {}, json.dumps(entity))
                    result = client.patch()                

                    if result.status_code not in [200, 201, 204]:
                        raise FcbgException("Unable to update entity on target CB. Response: " + str(result.status_code) + ", Reason: " + result.reason)
                except:
                    raise

            else: # Entity not in memory
                # Let's try to create it on the target CB
                self.create(entity)


    def __init__(self):
        '''
        Constructor
        '''        
        self.entities = []

        self.auth_token = None

        try:
            self.update_auth_token()
        except:
            raise
