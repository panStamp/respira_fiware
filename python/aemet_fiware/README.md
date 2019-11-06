# AEMET FIWARE bridge

This daemon periodically polls the AEMET service for updates in the weather measurements and pushes data to the FIWARE UltraLight IoT agent configured in config/config.py.

## sdnotify

Notifications against systemd. Install sdnotify with pip:

```
sudo pip3 install sdnotify
```

# Configuration

All configuration settings are contained into config/config.py. This file is self-explanatory.

# How to manually run program

Navigate to the folder where this program is stored and run the following command:

```
python3 aemet_fiware.py
```

# How to run program from systemctl

In order to start this program as a service on Linux boot, we need to follow these steps:

1. Modify aemet_fiware.service with the correct path to aemet_fiware.py

```
ExecStart=/usr/bin/python3 /path_to/aemet_fiware.py
```

2. Copy aemet_fiware.service to /lib/systemd/system/

3. Reload systemctl:

```
sudo systemctl daemon-reload
```

4. Enable and run new service:

```
sudo systemctl enable aemet_fiware.service
sudo systemctl start aemet_fiware.service
```

5. Finally check the status of your service as following command.

```
sudo systemctl status aemet_fiware.service
```

