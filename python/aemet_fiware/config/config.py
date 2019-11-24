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
# Date: Sep 20 2019
#########################################################################


class AfConfig(object):
    """
    AEMET FIWARE bridge configuration class
    """

    #####################################################################
    ## General settings
    #####################################################################

    ## Log enable
    LOG_ENABLE = False

    ## Process name
    PROC_NAME = "AEMET FIWARE bridge"

    ## Dictionary of parameters to be retrieved from service and the corresponding UltraLight nomenclature
    OBSERVATION_PARAMETERS = {"lat":"lat", "lon":"lon", "alt":"alt", "pres":"p", "ta":"t", "tamin":"tmin", "tamax":"tmax", "ts":"st", "hr":"h", "prec":"prec", "pliqt":"liqp", "psoltp":"solp", "inso":"inso", "vis":"vis", "tpr":"dp", "dmax":"wdmax", "dv":"wd", "vv":"ws", "vmax":"wsmax"}
    POLLUTION_PARAMETERS = {"SO2": "so2", "NO": "no", "NO2": "no2", "VEL": "ws", "DIR": "wd", "TEM": "t", "HUM": "h", "PRE": "p", "RAD": "rad", "LLU": "prec", "PM10": "pm10"}

    #####################################################################
    ## AEMET settings
    #####################################################################

    ## AEMET observation URL
    AEMET_OBSERVATION_URL = "https://opendata.aemet.es/opendata/api/observacion/convencional/datos/estacion/"
    
    ## AEMET pollution URL
    AEMET_POLLUTION_URL = "https://opendata.aemet.es/opendata/api/red/especial/contaminacionfondo/estacion/"

    ## AEMET API Key
    AEMET_APIKEY = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJkYmVyZW5ndWVyQHBhbnN0YW1wLmNvbSIsImp0aSI6ImIyZDNjZTAyLTYwMWYtNDg0OC04ZDAxLWUzNzVkMTUxNWQwNCIsImlzcyI6IkFFTUVUIiwiaWF0IjoxNTY4OTAzMzg1LCJ1c2VySWQiOiJiMmQzY2UwMi02MDFmLTQ4NDgtOGQwMS1lMzc1ZDE1MTVkMDQiLCJyb2xlIjoiIn0.kFtlI3b2vlKCNk247YHkxr2zgtiMh5K0O65R6rah_XI"

    ## List of station ID's to be queried for the observation data
    AEMET_STATION_IDS = ["4464X", "4489X", "4436Y", "5473X", "4478X", "4492F", "4325X", "4358X", "4520X", "4501X", "4244X", "4511C", "4386B", "4499X", "4410X", "4340", "4486X", "4260", "4468X", "4395X", "4497X", "4427X"]

    ## List of station ID's to be queried for the pollution data and their corresponding coordinates
    AEMET_POLLUTION_IDS = {"11": (38.515880, -6.856604)}

    #####################################################################
    ## FIWARE settings
    #####################################################################

    ## FIWARE service
    FIWARE_SERVICE = "openiot"

    ## FIWARE service group creation URL
    FIWARE_SERVGROUP_URL = "http://calidadmedioambiental.org/iot/services"

    ## FIWARE UL IoT agent URL
    FIWARE_UL_URL = "http://calidadmedioambiental.org/iot/d"

    ## FIWARE API Keys
    FIWARE_APIKEY_OBSERVATION = "5g4d8yt2d37gh12schq6l5z39d"
    FIWARE_APIKEY_POLLUTION = "BJm3UJFkapqZTu7m44fGjXRTJU"

    ## FIWARE entity names
    FIWARE_ENTITY_OBSERVATION = "AEMET_OBSERVATION"
    FIWARE_ENTITY_POLLUTION = "AEMET_POLLUTION"

    ## FIWARE datamodels
    FIWARE_DATAMODEL_OBSERVATION = {"lat":"latitude", "lon":"longitude", "alt":"altitude", "tiref":"refTime", "p":"pressure", "t":"temperature", "tmin":"minTemperature", "tmax":"maxTemperature", "st":"soilTemperature", "h":"humidity", "prec":"precipitation", "liqp":"liquidPrecipitation", "solp":"solidPrecipitation", "inso":"insolation", "vis":"visibility", "dp":"dewPoint", "wdmax":"maxWindDirection", "wd":"windDirection", "ws":"windSpeed", "wsmax":"maxWindSpeed"}
    FIWARE_DATAMODEL_POLLUTION = {"lat":"latitude", "lon":"longitude", "so2": "SO2", "no": "NO", "no2": "NO2", "ws": "windSpeed", "wd": "windDirection", "t": "temperature", "h": "humidity", "p": "pressure", "rad": "radiation", "prec": "precipitation", "pm10": "PM10"}

    ## Which iof the above parameters are strings
    FIWARE_DATAMODEL_STRINGS = []
