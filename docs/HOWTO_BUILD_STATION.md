[< back to index](../README.md)

# Index of contents

- [How to build your own RESPIRA FIWARE station](#how-to-build-your-own-respira-fiware-station)
- [Bills of materials](#bills-of-materials)
- [Assembly](#assembly)

# How to build your own RESPIRA FIWARE station

The following are the official bills of materials used in this project. If you don't find the exact references of course you can use your own ones. Since the spirit of this project is totally open source, users can build this station in very different ways, add improvements and even replace the sensors by new references.

# Bills of materials

Micorontroller unit:

| Reference | Description | Source |
|-----------|-------------|--------|
| U1 | 30-pin ESP32 NodeMCU board | e-bay, Amazon, Aliexpress, etc. |
|R1, R2 | 10kohm 1/6 W resistor | Mouser, Farnell, DigiKey, etc. |
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

All parts have been selected to avoid any surface mount soldering (SMT). This means that anyone with a minimum experience in soldering electronic parts and owning a soldering iron should be able to assemble this station.

[PICTURE]

Assembling the sensor block is quite simple as well. Sensor units need to be connected with wires to the piece of Ethernet cable by following this pinout:

<p align="center">
<img width="400" src="http://www.panstamp.org/pictures/respira_ethernet_pinout.jpg">
</p>

