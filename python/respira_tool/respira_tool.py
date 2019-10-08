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

    parser.add_argument("--list-service-groups",
                        action='store_true',
                        default= False,
                        help= "List all service groups under the same service and service path")

    parser.add_argument("--create-service-group",
                        action='store_true',
                        help= "Create service group with provided API key")

    parser.add_argument("--delete-service-group",
                        action='store_true',
                        help= "Delete service group with provided API key")

    parser.add_argument("--delete-all-service-groups",
                        action='store_true',
                        help= "Delete all service groups under the current service path")

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

    parser.add_argument("--list-devices",
                        action='store_true',
                        help= "List available devices")

    parser.add_argument("--read-device",
                        action='store_true',
                        help= "Read all values from device")

    parser.add_argument("--delete-device",
                        action='store_true',
                        help= "Delete device")

    parser.add_argument("--delete-all-devices",
                        action='store_true',
                        help= "Delete all devices under the current service path")

    parser.add_argument("--apikey",
                        "-k",
                        type= str,
                        help= "API key")

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
            result = fiware.list_service_groups()            
            print(json.dumps(result, indent=4, sort_keys=True))
            print("(" + str(len(result)) + " service groups)")

        elif args.show_service_path:
            print(fiware.read_service_path())

        elif args.set_service_path is not None:
            if args.set_service_path[0] != '/':
                print("Service path should start by character /")
            else:
                print("Service path set to " + args.set_service_path)
                fiware.set_service_path(args.set_service_path)

        elif args.create_service_group:
            if args.apikey is not None:
                if (len(args.apikey) != 26):
                    print("Incorrect length of API key. It should be 26 character length")
                else:
                    print("Creating service group...")
                    fiware.create_service_group(args.apikey)
                    print("Service group " + args.apikey + " successfully created")
            else:
                print("Please enter API key with option -k")

        elif args.delete_service_group:
            if args.apikey is not None:
                print("Deleting service group...")
                fiware.delete_service_group(args.apikey)
                print("Service group " + args.apikey + " successfully deleted")
            else:
                print("Please enter API key with option -k")

        elif args.delete_all_service_groups:
            print("Deleting all service groups...")
            result = fiware.delete_all_service_groups()
            print(str(result) + " service groups have been deleted")            

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

        elif args.list_devices:        
                print("Read device values:")
                result = fiware.list_devices()
                print(json.dumps(result, indent=4, sort_keys=True))
                print("(" + str(len(result)) + " devices)")

        elif args.read_device:        
            if args.device is not None:
                print("Read device values:")
                print("Device ID: " + args.device)
                result = fiware.read_device(args.device, args.show_values)
                print(json.dumps(result, indent=4, sort_keys=True))
            else:
                print("Please enter device ID with option -d")

        elif args.delete_device:        
            if args.device is not None:
                print("Delete device:")
                print("Device ID: " + args.device)
                fiware.delete_device(args.device)
                print("Device " + args.device + " successfully deleted")
            else:
                print("Please enter device ID with option -d")

        elif args.delete_all_devices:        
                print("Deleting all devices...")
                result = fiware.delete_all_devices()
                print(str(result) + " devices have been deleted")

    except RespException as ex:
        ex.show()
            

        