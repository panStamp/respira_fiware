# AEMET FIWARE bridge

This daemon periodically polls the AEMET service for updates in the weather measurements and pushes data to the FIWARE UltraLight IoT agent configured in config/config.py.

This program requires Python 3.6 or higher and the [sdnotify](https://pypi.org/project/sdnotify/) module to work

