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


class FcbgConfig(object):
    """
    FIWARE CB gateway config file
    """

    #####################################################################
    ## General settings
    #####################################################################

    ## Log enable
    LOG_ENABLE = True

    ## Process name
    PROC_NAME = "FIWARE CB gateway"
    
    ## HTTP server port
    HTTP_SERVER_PORT = 1812

    #####################################################################
    ## FIWARE settings
    #####################################################################

    ## SOURCE CB
    #####################################################################

    ## FIWARE subscription service
    FIWARE_SUBSCRIPTION_SERVICE = "openiot"

    ## FIWARE subscription service paths
    FIWARE_SUBSCRIPTION_SERVICE_PATHS = ["/RESPIRA"]

    ## FIWARE NGSI source subscription URL
    FIWARE_SUBSCRIPTION_URL = "http://localhost:1026/v2/subscriptions"

    ## FIWARE NGSI target URL
    FIWARE_TARGET_URL = "https://mytargetcb:10027/v2/entities"

    ## TARGET CB
    #####################################################################

    ## FIWARE target service
    FIWARE_TARGET_SERVICE = "badajozesmas"

    ## FIWARE target service path
    FIWARE_TARGET_SERVICE_PATH = "/Taller"

    ## Auth token URL
    FIWARE_AUTH_TOKEN_URL = "https://mytargetcb:15001/v3/auth/tokens"

    ## Time in seconds between token renewals
    FIWARE_AUTH_TOKEN_INTERVAL = 50 * 60

    ## User name
    FIWARE_TARGET_USER_NAME = "DanielB"

    ## User password
    FIWARE_TARGET_USER_PASSWORD = "badajozesmas"
