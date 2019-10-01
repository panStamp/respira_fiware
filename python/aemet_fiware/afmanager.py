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
from afaemet import AfAemet
from afiware import Afiware

import threading
import json
import time
import datetime


class AfManager(threading.Thread):
    """
    General IO management class
    """

    def run(self):
        """
        Start timer
        """
        # Endless loop
        while True:
            # Query pollution stations
            for loc_id, loc_coord in AfConfig.AEMET_POLLUTION_IDS.items():
                try:
                    aemet = AfAemet()                
                    (timestamp, ul_string) = aemet.query_pollution(loc_id, loc_coord)
                    print(ul_string)

                    if ul_string != "":
                        entity = AfConfig.FIWARE_ENTITY_POLLUTION + "_" + loc_id
                        Afiware(AfConfig.FIWARE_APIKEY_POLLUTION, entity, timestamp, ul_string)

                        date_time = datetime.datetime.now()
                        print(date_time.strftime("%Y-%m-%dT%H:%M:%S") + " : Pollution data successfully transmitted to FIWARE")
                except AfException as ex:
                    ex.show()

                time.sleep(5)

            # Query observation stations
            for loc in AfConfig.AEMET_STATION_IDS:
                try:
                    aemet = AfAemet()
                    (timestamp, ul_string) = aemet.query_observation(loc)
                    print(ul_string)

                    if ul_string != "":
                        entity = AfConfig.FIWARE_ENTITY_OBSERVATION + "_" + loc
                        Afiware(AfConfig.FIWARE_APIKEY_OBSERVATION, entity, timestamp, ul_string)

                        date_time = datetime.datetime.now()
                        print(date_time.strftime("%Y-%m-%dT%H:%M:%S") + " : Observation data successfully transmitted to FIWARE")
                except AfException as ex:
                    ex.show()

                time.sleep(5)

            # Trigger every hour at minute 05
            while datetime.datetime.now().minute != 5:
                time.sleep(60)


    def __init__(self):
        """
        Class constructor
        """
        threading.Thread.__init__(self)
        
        # Configure thread as daemon
        self.daemon = True
