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

import argparse
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

git     # Command-line parser
    parser = argparse.ArgumentParser(prog= "respira_tool",
                                    usage= "%(prog)s [command]",
                                    description= RespConfig.PROC_NAME,
                                    epilog= RespConfig.PROC_NAME + " " + VERSION)

    # Add arguments
    parser.add_argument("--list-service-groups",
                        action='store_true',
                        default= False,
                        help= "List all service groups under the same service and service path")

    parser.add_argument("--create-service-group",
                        type= str,
                        help= "Create service group for RESPIRA FIWARE")

    parser.add_argument("--delete-service-group",
                        type= str,
                        help= "Delete service group for RESPIRA FIWARE")

    parser.add_argument("--enable-zero-calibration",
                        choices=["no2", "pm"],
                        help= "Enable zero automatic calibration for sensor")

    parser.add_argument("--disable-zero-calibration",
                        choices=["no2", "pm"],
                        help= "Disable zero automatic calibration for sensor")

    parser.add_argument("--reset-calibration",
                        action='store_true',
                        help= "Reset calibration settings to defaults")

    parser.add_argument("--calibrate",
                        choices=["no2", "pm1.0", "pm2.5", "pm4.0", "pm10"],
                        help= "Enter calibration factor and offset for polluant")

    parser.add_argument("--read-device",
                        action='store_true',
                        help= "Read all values from device")

    parser.add_argument("--device",
                        "-d",
                        type= str,
                        help= "Device ID")

    parser.add_argument("--factor",
                        "-f",
                        type= float,
                        default= 1.0,
                        help= "Calibration factor (default factor = 1)")

    parser.add_argument("--offset",
                        "-o",
                        type= float,
                        default= 0.0,
                        help= "Calibration offset (default offset = 0)")

    parser.add_argument("--show-values",
                        action='store_true',
                        default= False,
                        help= "Show only values when retrieving entity attributes from CB")


    # Execute the parse_args() method
    args = parser.parse_args()

    try:
        # RESPIRA FIWARE object
        fiware = RespFiware()

        if args.list_service_groups:
            print("Listing service groups...")
            print(fiware.list_service_groups())

        elif args.create_service_group is not None:
            api_key = args.create_service_group
            if (len(api_key) != 26):
                print("Incorrect length of API key. It should be 26 character length")
            else:
                print("Creating service group...")
                fiware.create_service_group(api_key)

        elif args.delete_service_group is not None:
            api_key = args.delete_service_group
            if (len(api_key) != 26):
                print("Incorrect length of API key. It should be 26 character length")
            else:
                print("Deleting service group...")
                fiware.delete_service_group(api_key)

        elif args.enable_zero_calibration is not None:
            if args.device is not None:
                print("Enabling automatic zero calibration:")
                print("Device ID: " + args.device)
                print("Sensor: " + args.enable_zero_calibration)

                fiware.enable_zero_calibration(args.device, args.enable_zero_calibration)
            else:
                print("Please enter device ID with option -d")

        elif args.disable_zero_calibration is not None:
            if args.device is not None:
                print("Disabling automatic zero calibration:")
                print("Device ID: " + args.device)
                print("Sensor: " + args.disable_zero_calibration)

                fiware.disable_zero_calibration(args.device, args.disable_zero_calibration)
            else:
                print("Please enter device ID with option -d")

        elif args.reset_calibration:        
            if args.device is not None:
                print("Reset calibration settings to default values:")
                print("Device ID: " + args.device)

                fiware.reset_calibration(args.device)
            else:
                print("Please enter device ID with option -d")

        elif args.calibrate is not None:        
            if args.device is not None:
                print("Writing calibration settings:")
                print("Device ID: " + args.device)
                print("Polluant: " + args.calibrate)
                print("Calibration factor = " + str(args.factor))
                print("Calibration offset = " + str(args.offset))

                fiware.calibrate(args.device, args.calibrate, args.factor, args.offset)
            else:
                print("Please enter device ID with option -d")

        elif args.read_device:        
            if args.device is not None:
                print("Read device values:")
                print("Device ID: " + args.device)
                print(fiware.read_device(args.device, args.show_values))
            else:
                print("Please enter device ID with option -d")

    except RespException as ex:
        ex.show()
            

        