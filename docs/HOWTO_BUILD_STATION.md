[< back to index](../README.md)

# Index of contents

- [How to build your own RESPIRA FIWARE station](#how-to-build-your-own-respira-fiware-station)
- [Bills of materials](#bills-of-materials)
- [Assembly](#assembly)
- [Programming](#programming)

# How to build your own RESPIRA FIWARE station

The following are the official bills of materials used in this project. If you don't find the exact references of course you can use your own ones. Since the spirit of this project is totally open source, users can build this station in very different ways, add improvements and even replace the sensors by new references.

# Bills of materials

Users are invited to make their own PCB's based on the available schematics or source the boards from [OSHPARK](https://oshpark.com/).

Microntroller unit:

| Reference | Description | Source |
|-----------|-------------|--------|
| U1 | 30-pin ESP32 NodeMCU board | e-bay, Amazon, Aliexpress, etc. |
| R1, R2 | 10kohm 1/6 W resistor | Mouser, Farnell, DigiKey, etc. |
| C1 | 1uF 10V ceramic capacitor | Mouser, Farnell, DigiKey, etc. |
| C2 | 100nF 10V ceramic capacitor | Mouser, Farnell, DigiKey, etc. |
| J1 | 2-pos 5mm-pitch screw connector | Mouser, Farnell, DigiKey, etc. |
| J4 | Molex 95503-2881 Vertical RJ45 connector | Mouser, Farnell, DigiKey, etc. |
| Enclosure | FIBOX TEMPO TAM131007 | RS, Farnell, etc. |

Sensor unit:

| Reference | Description | Source |
|-----------|-------------|--------|
| SI7021 | SI7021 dual temperature and humidity sensor | e-bay, Amazon, Aliexpress, etc. |
| SPS30 | Sensirion particulate matter sensor | Mouser, Farnell, DigiKey, etc. |
| SPS30 connector | ZH 1.5mm JST 5-pole female connector | e-bay, Mouser, Farnell, Digikey, etc. |
| Enclosure | TFA-Dostmann 98.1114.02 | Amazon |
| Ethernet cable | 30 cm of CAT-6 8-pole Ethernet cable | Local store |
| Monopole wire | Coloured <=0.5mm monopole wire | Local store |

# Assembly

All parts have been selected to avoid any surface mount soldering (SMT). This means that anyone with a minimum experience in soldering electronic parts and owning a soldering iron should be able to assemble this station. The main microcontroller board is shown in the image below:

[PICTURE of MCU board]

Assembling the sensor board is quite simple as well. Sensor units need to be connected to the auxiliary sensor board with wires. Finally, the sensor board is fixed into the pagoda-style enclosure and connected to the main microcontroller board by means of an Ethernet cable.

[PICTURE of sensor board]

The following pinout diagram is recommended for the Ethernet cable:

<p align="center">
<img width="400" src="http://www.panstamp.org/pictures/respira_ethernet_pinout.jpg">
</p>

This image shows a complete RESPIRA FIWARE station completely assembled:

[PICTURE of RESPIRA station]

# Programming

The ESP32 is programmed from the [Arduino IDE](https://www.arduino.cc/). Simply select the board _ESP32 Dev board_ from Tools->Boards, connect the ESP32 board to your computer via USB, select the right serial port and upload the code to the board. The source code is ready with the right API Key to connect RESPIRA to the [Environmental Open Labs](OPEN_LABS.md). However, if you want to connect the station to a different FIWARE service, then change the API Key accordingly.

From ]respira_fiware.ino](https://github.com/panStamp/respira_fiware/blob/master/arduino/respira_fiware/respira_fiware.ino):

```C++
const char FIWARE_SERVER[] = FIWARE_SERVER_IP_ADDRESS;
const uint16_t FIWARE_PORT = FIWARE_UL_PORT;
const char FIWARE_APIKEY[] = FIWARE_UL_API_KEY;
```

