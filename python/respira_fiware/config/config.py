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
    PROC_NAME = "RESPIRA FIWARE service group creator"
    
    #####################################################################
    ## FIWARE settings
    #####################################################################

    ## FIWARE service
    FIWARE_SERVICE = "openiot"

    ## FIWARE service group creation URL
    FIWARE_SERVGROUP_URL = "http://63.35.250.27:4041/iot/services"

    ## FIWARE API Key
    FIWARE_APIKEY = "si95g7noxpmah9cbx9ggoe36vv"

    ## FIWARE entity names
    FIWARE_ENTITY = "RESPIRA"

    ## FIWARE datamodel
    FIWARE_DATAMODEL = {"t":"temperature", "h":"humidity", "no2": "NO2", "pm1": "PM1.0", "pm2": "PM2.5", "pm4": "PM4.0", "pm10": "PM10", "typs": "typicalSize"}

    ## Which of the above parameters are strings
    FIWARE_DATAMODEL_STRINGS = []

