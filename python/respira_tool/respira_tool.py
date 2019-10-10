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
from config import RespConfig

import argparse
import sys
import os
import time
import signal
import json


VERSION = "0.1.0"


def signal_handler(signal, frame):
    """
    Handle signal received
    """
    sys.exit(0)


if __name__ == '__main__':
   
    # Catch possible SIGINT signals
    signal.signal(signal.SIGINT, signal_handler)

    fiware = RespFiware()
    fiware.enable_zero_calibration("RESPIRA_807D3AF39E18", "pm")

    # Command-line parser
    parser = argparse.ArgumentParser(prog= "respira_tool",
                                    usage= "%(prog)s [command]",
                                    description= RespConfig.PROC_NAME,
                                    epilog= RespConfig.PROC_NAME + " " + VERSION)

    # Add arguments
    parser.add_argument("--show-service-path",
                        action='store_true',
                        help= "Show service path")

    parser.add_argument("--set-service-path",
                        type=str,
                        help= "Set service path")

    parser.add_argument("--read-calibration",
                        action='store_true',
                        help= "Show calibration settings for a device")

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

    parser.add_argument("--device",
                        "-d",
                        type= str,
                        help= "Device ID (<device type>:<device id>)")

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

    # Execute the parse_args() method
    args = parser.parse_args()

    try:
        # RESPIRA FIWARE object
        fiware = RespFiware()

        if args.show_service_path:
            print(fiware.read_service_path())

        elif args.set_service_path is not None:
            if args.set_service_path[0] != '/':
                print("Service path should start by character /")
            else:
                print("Service path set to " + args.set_service_path)
                fiware.set_service_path(args.set_service_path)        

        elif args.enable_zero_calibration is not None:
            if args.device is not None:
                print("Enabling automatic zero calibration:")
                print("Device ID: " + args.device)
                print("Sensor: " + args.enable_zero_calibration)

                fiware.enable_zero_calibration(args.device, args.enable_zero_calibration)
                print("Zero calibration enabled for device " + args.device)
            else:
                print("Please enter device ID with option -d")

        elif args.disable_zero_calibration is not None:
            if args.device is not None:
                print("Disabling automatic zero calibration:")
                print("Device ID: " + args.device)
                print("Sensor: " + args.disable_zero_calibration)

                fiware.disable_zero_calibration(args.device, args.disable_zero_calibration)
                print("Zero calibration disabled for device " + args.device)
            else:
                print("Please enter device ID with option -d")

        elif args.reset_calibration:        
            if args.device is not None:
                print("Reset calibration settings to default values:")
                print("Device ID: " + args.device)

                fiware.reset_calibration(args.device)
                print("Calibration set to default values for device " + args.device)
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
                print("Calibration saved for device " + args.device)
            else:
                print("Please enter device ID with option -d")

        elif args.read_calibration:
            if args.device is not None:
                print("Calibration settings for device " + args.device)

                fiware.print_calibration(args.device)
            else:
                print("Please enter device ID with option -d")

    except RespException as ex:
        ex.show()
            

        