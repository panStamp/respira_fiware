[< back to index](../../README.md)

# Index of contents

- [The RESPIRA FIWARE station](#the-respira-fiware-station)
- [Specifications](#specifications)
- [Components](#components)
  - [Microcontroller unit](#microcontroller-unit)
  - [Sensors](#sensors)

# The RESPIRA FIWARE station

The RESPIRA hardware follows a simple architecture. An ESP32 SoC acts as the brain of the environmental station. Ambient temperature, relative humidity, NO2 concentration and particle matter (PM) are read from three external sensors via I2C and UART. The ESP32 has sufficient space in flash and horsepower to internally store and process readings in order to filter levels and periodically run some calibration routines. Finally, processed information is transmitted to the FIWARE platform via a [HTTP UltraLight 2.0 request](https://fiware-iotagent-ul.readthedocs.io/en/latest/usermanual/index.html).

# Specifications

- Parameters provided: Temperature, humidity, NO2, PM1.0, PM2.5, PM4.0 and PM10
- Power supply : 5.0VDC
- Maximum current consummed : 300 mA
- Communication : WiFi 2.4GHz
- FIWARE protocol: UltraLight 2.0 HTTP

# Components

RESPIRA FIWARE is formed by two main blocks. The first block is the microcontroller unit, the core of the solution containing the ESP32 board and and the necessary connectivity. The second block is the sensing element, a pagoda-style enclosure containing the environmental sensors. Both main components communicate between them via UART and I2C.

## Microcontroller unit

This board relies only on "through-hole" (THT) components in order to simplify the assembly and let the community build RESPIRA stations on basic prototyping boards. As result, we have then chosen an ESP32 NodeMCU board as the ESP32 core. This board not only contains an ESP32 SoC but also a USB interface, used to program and debug the SoC, an on-board 3.3 VDC PSU and a couple of push buttons to manually put the board in programming mode.

<p align="center">
<img width="400" src="http://www.panstamp.org/pictures/NODEMCU-ESP32-01.png">
</p>

The microcontroller board fits into a FIBOX TEMPO TAM131007 box on the left side whilst keeping the right side of the enclosure free in case the user decides to add connectivity for some additional sensors or even place a 5VDC power supply.

## Sensors

Sensors are assembled into a pagoda-style enclosure in order to achive the best passive ventilation. We have chosen for this project the TFA-Dostmann 98.1114.02 enclosure, usually available on Amazon.

RESPIRA relies on three external sensors, which have been retained for their accuracy, stability and communication capabilities.

### [SI7021](https://www.silabs.com/documents/public/data-sheets/Si7021-A20.pdf) Temperature and Humidity sensor

This IC made by Silicon Labs is an exceptional dual temperature-humidity sensor that can be operated via I2C. There are lots of Arduino libraries for this sensor and is also available in form of breakout board so that there is no need to do any surface soldering. These boards are available on eBay and Aliexpress for less than 4 EUR.

<p align="center">
<img width="300" src="http://www.panstamp.org/pictures/si7021.png">
</p>

### [SPS30](https://www.sensirion.com/en/environmental-sensors/particulate-matter-sensors-pm25/) Particulate Matter sensor

SPS30 is an advanced compact particulate matter sensor designed and manufactured by Sensirion. It is capable to detect particles from 0.5 to 10 microns, calculate concentration for each diameter and even calculate the total mass per diameter. SPS30 features a small package (41x41x12mm) and provides connectivity via UART and I2C. SPS30 is available on Mouser and Digikey for around 40 EUR in small quantities.

<p align="center">
<img width="500" src="http://www.panstamp.org/pictures/SPS30.jpg">
</p>

The following parameters are obtained from the SPS30 sensor:

- Concentration of PM1.0, PM2.5, PM4.0 and PM10
- Total average size of particules detected

### [ECS1-NO2-50](http://pmo0ec072.pic33.websiteonline.cn/upload/ES1-NO2-50_20171212.pdf) NO2 sensor

ES1-NO2-50 is an electrochemical NO2 sensor sensible in the 0 to 50 ppm range. Of course we dont need that full range but the sensor performs quite well in low concentrations of gas. Moreover, the zero drift is minimum and the sensor comes calibrated from factory. In order to simplify the integration of this tiny sensor, it can be plugged onto a TB600 board, which does all the complex analog transformations and provides a clean digital reading via UART.

<p align="center">
<img width="500" src="http://www.panstamp.org/pictures/tb600.png">
</p>

ES1-NO2-50 and TB600 are manufactured by ECSense and can be purchased from Pewatron, the official distributor of ECSense in Europe. Price is around 120 EUR for single quantities.

