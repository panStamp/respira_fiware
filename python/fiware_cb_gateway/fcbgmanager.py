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

from config.config import FcbgConfig
from fcbgexception import FcbgException
from fcbghttpserver import FcbgHttpServer
from fcbgupdater import FcbgUpdater
from fcbgsubscriber import FcbgSubscriber

import threading
import json
import time
import datetime


class FcbgManager(threading.Thread):
    """
    General IO management class
    """

    def notify(self, notification):
        """
        Receive notification from HTTP server
        """
        if "data" in notification:
            for entity in notification["data"]:
                if "federate" in entity: 
                    if "value" in entity["federate"]:
                        if entity["federate"]["value"].lower() == "true":
                            del entity["federate"]
                            try:
                                self.updater.update(entity)
                            except FcbgException as ex:
                                ex.show()


    def run(self):
        """
        Start timer
        """
        # Endless loop
        while True:
            pass


    def __init__(self):
        """
        Class constructor
        """
        threading.Thread.__init__(self)
        
        ## Configure thread as daemon
        self.daemon = True
        
        try:
            ## HTTP server
            server = FcbgHttpServer(self)
            server.start()
            
            ## NGSI subscriber
            FcbgSubscriber()

            ## NGSI updater
            self.updater = FcbgUpdater()
        
        except FcbgException as ex:
            ex.show()


