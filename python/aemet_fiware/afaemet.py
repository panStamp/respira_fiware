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
from datetime import datetime


class AfAemet(object):
    """
    AEMET HTTP agent
    """


    def query_observation(self, location):
        '''
        Query observation data

        @param location: location id of the AEMET station

        @return UL string to be passed to the FIWARE agent
        '''
        ## UltraLight string to be generated from request
        ul_string = ""

        ## Ask for data URL
        try:
            url = AfConfig.AEMET_OBSERVATION_URL + location
            params = {"api_key" : AfConfig.AEMET_APIKEY}
            headers = {"Accept" : "application/json", "Content-Type": "application/json"}
            client = AfHttpClient(headers, url, params)
            res = client.get()
            data_url = res["datos"]

            ## Ask for observation data
            try:
                client = AfHttpClient(headers, data_url)
                res = client.get()

                try:
                    last_time = datetime.strptime("2000-01-01T00:00:00", "%Y-%m-%dT%H:%M:%S")
                    last_measurement = None
                    ## Get last readings from result
                    for measurement in res:
                        if "fint" in measurement:
                            timestamp = datetime.strptime(measurement["fint"], "%Y-%m-%dT%H:%M:%S")
                            if timestamp > last_time:
                                last_time = timestamp
                                last_measurement = measurement

                    if last_measurement is not None:                       
                        for param, ul_key in AfConfig.OBSERVATION_PARAMETERS.items():
                            if param in last_measurement:
                                value = last_measurement[param]

                                if ul_key in AfConfig.FIWARE_DATAMODEL_STRINGS:
                                    pos = value.find(" (")
                                    if pos > -1:
                                        value = value[0:pos]

                                if ul_string != "":
                                    ul_string += "#"
                                ul_string += ul_key + "|" + str(value)

                        return (timestamp, ul_string)

                except:
                    raise AfException("Unable to parse observation data from " + data_url)

            except:
                raise AfException("Unable to get observation data from " + data_url)
        except:
            raise AfException("Unable to get data URL from " + url)

        return None


    def query_pollution(self, loc_id, loc_coord):
        '''
        Query pollution data

        @param loc_id: location id of the AEMET station
        @param loc_coord: location coordinates of the AEMET station

        @return UL string to be passed to the FIWARE agent
        '''
        ## UltraLight string to be generated from request
        ul_string = ""

        ## Ask for data URL
        try:
            url = AfConfig.AEMET_POLLUTION_URL + loc_id
            params = {"api_key" : AfConfig.AEMET_APIKEY}
            headers = {"Accept" : "application/json", "Content-Type": "application/json"}
            client = AfHttpClient(headers, url, params)
            res = client.get()
            data_url = res["datos"]

            ## Ask for observation data
            try:
                client = AfHttpClient(headers, data_url)
                res = client.get()               
                lines = res.splitlines()

                # Get last tine (most recent reading)
                last_line = lines[-1]

                print("Last line:")
                print(last_line)

                # Get timestamp
                date_time = last_line[0:16]
                print(date_time)
                timestamp = datetime.strptime(date_time, "%d-%m-%Y %H:%M")
                ul_string = "tiref|" + timestamp.strftime("%Y-%m-%dT%H:%M:%S")
                ul_string += "#lat|" + str(loc_coord[0]) + "#lon|" + str(loc_coord[1])

                for param, ul_key in AfConfig.POLLUTION_PARAMETERS.items():
                    pos = last_line.find(param)
                    if (pos > -1):
                        pos = last_line.find(": +", pos)
                        str_val = last_line[pos+3 : pos+11]

                        try:
                            value = float(str_val)
                            ul_string += "#" + ul_key + "|" + str(value)
                        except:
                            pass

                return (timestamp, ul_string)

            except:
                raise AfException("Unable to get pollution data from " + data_url)
        except:
            raise AfException("Unable to get data URL from " + url)

        return None


    def __init__(self):
        '''
        Constructor
        '''
        pass
