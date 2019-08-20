[< back to index](../README.md)

# The challenge

RESPIRA Fiware is an open source air monitoring device for urban applications. It is an evolution from precedent versions of RESPIRA designed by the company [panStamp](http://www.panstamp.com) and being deployed by the community since 2013. This version of RESPIRA has been created under the scope of the FIWARE IoT challenge 2019 launched by [Diputación de Badajoz](https://www.dip-badajoz.es/) and [Telefónica](https://www.telefonica.com/en/) by means of [FIWARE Space](https://www.fiware.space/).

# FIWARE

FIWARE is an international standard created to become the core of interoperable IoT (Internet Of Things) platforms. It is based on popular technologies such as HTTP and MongoDB and relies on a well defined M2M architecture where the Orion Context Broker, the central piece of this architecture, handles information from many different heterogeneous IoT systems.

Fiware has been deployed in many Smart City projects around the world and is compatible with dozens of IoT technologies and data management platforms. RESPIRA Fiware is able to transmit air pollution levels to any FIWARE-powered platform via an [HTTP UltraLight IoT agent](https://fiware-iotagent-ul.readthedocs.io/en/latest/usermanual/index.html).

Please refer to the official [FIWARE web page](https://www.fiware.org/) for more information about this technology.

# RESPIRA

RESPIRA follows a very simple concept. The core, an ESP32 SoC, reads temperature, humidity, particle matter and No2 levels periodically from three sensors. Readings are then stored and processed locally in the MCU and then transmitted to a FIWARE platform. The default settings make the RESPIRA station transmit to the _Environmental Open Labs_ but developers cah change these settings to point to a different FIWARE platform.

This project contains all the necessary source code and instructions to build and deploy new RESPIRA stations. Go to [this guiding page](RESPIRA_STATION.md) for more details about how the RESPIRA hardware works and how to build your own station.

# Environmental Open Labs

_Environmental Open Labs_ is another open initiative of [Diputación de Badajoz](https://www.dip-badajoz.es/) and [Telefónica](https://www.telefonica.com/en/) based on FIWARE to collect, display and exploit data from many different environmental IoT sources in the Spanish province of Badajoz. This on-line platform has also been developped by [panStamp](http://www.panstamp.com) and is part of the FIWARE IoT challenge 2019 won by the company.

Open [this page](OPEN_LABS.md) to know something more about the Environmental Open Labs.

