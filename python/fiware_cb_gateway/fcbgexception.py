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

import logging
import os


class FcbgException(Exception):
    """
    Main exception class
    """

    ## Path to the log file
    LOGFILE = "log/exceptions.log"

    def show(self):
        """
        Print short exception description
        """
        print (self.description)
        

    def log(self):
        """
        Write exception in log file
        """
        logging.basicConfig(filename=FcbgException.LOGFILE, filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')
        logging.error(self.description)
        

    @staticmethod
    def clear():
        """
        Clear error file
        """
        # Remove existing error file
        if os.path.exists(FcbgException.LOGFILE):
            os.remove(FcbgException.LOGFILE)


    def __init__(self, value):
        """
        Class constructor
        
        @param value: Description about the error
        """
        # Exception description
        self.description = value

        # Log exception
        if FcbgConfig.LOG_ENABLE:
            self.log()
  
