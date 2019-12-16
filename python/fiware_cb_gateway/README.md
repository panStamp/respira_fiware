# FIWARE Context-Broker gateway

This daemon updates entities from a source CB to a target CB. The process keeps itself subscribed to the source CB and updates changes on the target CB via the [NGSI /V2/entities API](https://fiware-orion.readthedocs.io/en/master/user/walkthrough_apiv2/index.html)


## Previous requirements

Notifications against systemd. Install sdnotify with pip:

```
sudo pip3 install sdnotify
```

And then install cherrypy:

```
sudo pip3 install cherrypy
```

# Configuration

All configuration settings are contained into config/config.py. This file is self-explanatory.

# How to manually run program

Navigate to the folder where this program is stored and run the following command:

```
python3 fiware_cb_gateway.py
```

# How to run program from systemctl

In order to start this program as a service on Linux boot, we need to follow these steps:

1. Modify fiware_cb_gateway.service with the correct path to fiware_cb_gateway.py

```
ExecStart=/usr/bin/python3 /path_to/fiware_cb_gateway.py
```

2. Copy eea_fiware.service to /lib/systemd/system/

3. Reload systemctl:

```
sudo systemctl daemon-reload
```

4. Enable and run new service:

```
sudo systemctl enable fiware_cb_gateway.service
sudo systemctl start fiware_cb_gateway.service
```

5. Finally check the status of your service as following command.

```
sudo systemctl status fiware_cb_gateway.service
```

