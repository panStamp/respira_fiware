#########################################################################
# Copyright (c) 2018 panStamp <contact@panstamp.com>
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

import requests


class FcbgHttpClient(object):
    """
    HTTP client
    """

    def get(self):
        """
        Run HTTP get request
        """
        try:
            return requests.get(self.url, headers=self.header, params=self.parameters, data=self.payload, verify=False)
        except Exception as ex:
            raise FcbgException(str(ex))


    def post(self):
        """
        Run HTTP post request
        """
        try:
            return requests.post(self.url, headers=self.header, params=self.parameters, data=self.payload, verify=False)
        except Exception as ex:
            raise FcbgException(str(ex))


    def patch(self):
        """
        Run HTTP patch request
        """
        try:
            return requests.patch(self.url, headers=self.header, params=self.parameters, data=self.payload, verify=False)
        except Exception as ex:
            raise FcbgException(str(ex))


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
