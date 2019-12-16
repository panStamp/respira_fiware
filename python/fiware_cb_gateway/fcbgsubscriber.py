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
# Date: Dec 16 2019
#########################################################################

from config.config import FcbgConfig
from fcbgexception import FcbgException
from fcbghttpclient import FcbgHttpClient

import json


class FcbgSubscriber(object):
    """
    FIWARE NGSI subscriber
    """

    def create(self, service_path):
        """
        Create subscription on source CB

        @param service_path : service path to get notifications from
        """
        url = FcbgConfig.FIWARE_SUBSCRIPTION_URL
        headers = {
            "fiware-service": FcbgConfig.FIWARE_SUBSCRIPTION_SERVICE,
            "fiware-servicepath": service_path,
            "Content-type" : "application/json"
            }

        body = {
            "description": "Full subscription to " + service_path,
            "subject":
            {
                "condition" : {"attrs": []}
            },
            "notification":
            {
                "http": {"url": "http://localhost:1812/notify"},
                "attrs": []
            }
        }

        try:
            client = FcbgHttpClient(headers, url, {}, body)
            result = client.post()

            if result.status_code not in [200, 201]:
                raise FcbgException("Unable to create subscription on source CB. Response: " + str(result.status_code) + ", Reason: " + result.reason)
        except:
            raise


    def check(self, service_path):
        """
        Check if subscription exists or not

        @param service_path : service path to check the notification from

        @return True if subscription already exists. Return False otherwise
        """
        url = FcbgConfig.FIWARE_SUBSCRIPTION_URL
        headers = {
            "fiware-service": FcbgConfig.FIWARE_SUBSCRIPTION_SERVICE,
            "fiware-servicepath": service_path,
            "Content-type" : "application/json"
            }

        try:
            client = FcbgHttpClient(headers, url, {}, "")
            result = client.get()

            if result.status_code not in [200, 201]:
                raise FcbgException("Unable to get subscriptions from source CB. Response: " + str(result.status_code) + ", Reason: " + result.reason)

            try:
                subscriptions = json.loads(result.text)
                if len(subscriptions) > 0:
                    return True
                else:
                    return False
            except:
                raise FcbgException("Response from CB is not a JSON object:\n" + result.text)
        except:
            raise


    def __init__(self):
        '''
        Constructor
        '''        
        self.entities = []

        self.auth_token = None

        try:
            for service_path in FcbgConfig.FIWARE_SUBSCRIPTION_SERVICE_PATHS:
                if not check(service_path):
                    create(service_path)
        except:
            raise
