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
from respfiware import RespFiware
from config.config import RespConfig

import sys
import os
import time
import signal


VERSION = "0.1.0"


def signal_handler(signal, frame):
    """
    Handle signal received
    """
    sys.exit(0)


if __name__ == '__main__':
   
    # Catch possible SIGINT signals
    signal.signal(signal.SIGINT, signal_handler)

    print(RespConfig.PROC_NAME + " " + VERSION)

    try:
        fiware = RespFiware()
        fiware.create_service_group(RespConfig.FIWARE_APIKEY, RespConfig.FIWARE_ENTITY, RespConfig.FIWARE_DATAMODEL)
    except RespException as ex:
        ex.show()
        