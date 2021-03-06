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

import json
import requests


class AfHttpClient(object):
    """
    HTTP client
    """

    def get(self):
        """
        Run HTTP get request
        """
        try:
            result = requests.get(self.url, headers=self.header, params=self.parameters, data=self.payload)

            if result.status_code == 200:
                try:
                    return result.json()
                except:
                    return result.text
            else:
                raise AfException("Unable to reach server via HTTP. Status: " + result.status_code + " . Reason: " + result.reason)

        except Exception as ex:
            raise AfException(str(ex))

    def post(self):
        """
        Run HTTP post request
        """
        try:
            result = requests.post(self.url, headers=self.header, params=self.parameters, data=self.payload)

            if result.status_code in [200, 201]:
                try:
                    return result.json()
                except:
                    return result.text
            else:
                raise AfException("Unable to reach server via HTTP. Status: " + result.status_code + " . Reason: " + result.reason)

        except Exception as ex:
            raise AfException(str(ex))


    def __init__(self, header, url, params="", payload=""):
        '''
        Constructor

        @param header: Dictionary of HTTP request headers
        @param url: URL to be reached
        @param params: Dictionary of HTTP request parameters
        @param payload: HTTP payload
        '''
        ## HTTP headers
        self.header = header

        ## URL
        self.url = url

        ## HTTP parameters
        self.parameters = params

        ## HTTP payload
        self.payload = payload


if __name__ == '__main__':

    api_key = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJkYmVyZW5ndWVyQHBhbnN0YW1wLmNvbSIsImp0aSI6ImIyZDNjZTAyLTYwMWYtNDg0OC04ZDAxLWUzNzVkMTUxNWQwNCIsImlzcyI6IkFFTUVUIiwiaWF0IjoxNTY4OTAzMzg1LCJ1c2VySWQiOiJiMmQzY2UwMi02MDFmLTQ4NDgtOGQwMS1lMzc1ZDE1MTVkMDQiLCJyb2xlIjoiIn0.kFtlI3b2vlKCNk247YHkxr2zgtiMh5K0O65R6rah_XI"
    location_id = "4358X"
    url = "https://opendata.aemet.es/opendata/api/observacion/convencional/datos/estacion/" + location_id #+ "?api_key=" + api_key
    params = {"api_key" : api_key}
    headers = {"Accept" : "application/json"}
    client = AfHttpClient(headers, url, params)
    res = client.get()
    print(res)
