# Basic FIWARE temperature and humidity sensor

This is a basic example showing how to connect a temperature and humidity sensor to our RESPIRA open platform via FIWARE UltraLight. The source code is ready to upload to a ESP8266 SoC from an Arduino IDE. The sensor is a SI7021 dual temperature and humidity sensor supporting I2C communications.

## Necessary steps before compiling:

1. Install ESP8266 Arduino cores from the Arduino boards manager by following this guide: 
https://github.com/esp8266/Arduino#installing-with-boards-manager

2. Install SparkFun's SI7021 library from the Arduino library manager:
https://github.com/sparkfun/SparkFun_Si701_Breakout_Arduino_Library

3. Install WiFi Manager by tzapu also from the Arduino library manager:
https://github.com/tzapu/WiFiManager#install-through-library-manager

