# EEA FIWARE bridge

This daemon periodically (hourly) polls the European Environment Agency (EEA) service for updates in the pollution measurements and pushes data to the FIWARE UltraLight IoT agent configured in config/config.py.

This program requires Python 3.7 and the [sdnotify](https://pypi.org/project/sdnotify/) module to work
