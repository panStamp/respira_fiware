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

from respexception import RespException

import os
import json


class RespConfig(object):
    """
    RESPIRA FIWARE configuration class
    """

    #####################################################################
    ## General settings
    #####################################################################

    ## Log enable
    LOG_ENABLE = False

    ## Process name
    PROC_NAME = "RESPIRA FIWARE command-line tool"
    
    ## List of polluants
    POLLUANTS = ["no2", "pm1.0", "pm2.5", "pm4.0", "pm10"]

    ## Config file
    CONFIG_FILE = "config.json"

    #####################################################################
    ## FIWARE settings
    #####################################################################

    ## FIWARE service
    FIWARE_SERVICE = "openiot"

    ## FIWARE service path
    FIWARE_SERVICE_PATH = "/RESPIRA_T5"

    ## FIWARE service group creation URL
    FIWARE_SERVGROUP_URL = "http://63.35.250.27:4041/iot/services"

    ## FIWARE entity query URL
    FIWARE_ENTITIES_URL = "http://63.35.250.27:1026/v2/entities"

    ## FIWARE entity name
    FIWARE_ENTITY_TYPE = "RESPIRA"

    ## FIWARE datamodel
    FIWARE_DATAMODEL = {"t":"temperature", "h":"humidity", "no2": "NO2", "pm1": "PM1.0", "pm2": "PM2.5", "pm4": "PM4.0", "pm10": "PM10", "typs": "typicalSize", "q": "airQualityIndex"}

    ## Which of the above parameters are strings
    FIWARE_DATAMODEL_STRINGS = []

    @staticmethod
    def save_config():
        """
        Save config in json file
        """
        config = {
                "FIWARE_SERVICE": RespConfig.FIWARE_SERVICE,
                "FIWARE_SERVICE_PATH": RespConfig.FIWARE_SERVICE_PATH,
                "FIWARE_SERVGROUP_URL": RespConfig.FIWARE_SERVGROUP_URL,
                "FIWARE_ENTITIES_URL": RespConfig.FIWARE_ENTITIES_URL
               }

        try:
            config_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "config", RespConfig.CONFIG_FILE)

            with open(config_path, 'w', encoding='utf-8') as config_file:
                json.dump(config, config_file, ensure_ascii=False, indent=4)
        except Exception as ex:
            print(str(ex))
            raise RespException("Unable to save configuration")


    @staticmethod
    def load_config():
        """
        Read config from json file
        """
        try:
            config_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "config", RespConfig.CONFIG_FILE)

            with open(config_path) as config_file:
                config = json.load(config_file)

            RespConfig.FIWARE_SERVICE = config["FIWARE_SERVICE"]
            RespConfig.FIWARE_SERVICE_PATH = config["FIWARE_SERVICE_PATH"]
            RespConfig.FIWARE_SERVGROUP_URL = config["FIWARE_SERVGROUP_URL"]
            RespConfig.FIWARE_ENTITIES_URL = config["FIWARE_ENTITIES_URL"]

        except:
            raise RespException("Unable to read configuration")
