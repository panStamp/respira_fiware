[< back to index](../../README.md)

# Index of contents

- [RESPIRA tool](#respira-tool)
- [Manual factor-offset correction](#manual-factor-offset-correction)
- [Automatic zero-level correction](#automatic-zero-level-correction)
- [Reset calibration values](#reset-calibration-values)

# RESPIRA tool

RESPIRA tool is a command-line program written in Python 3.7 to send configuration and calibration settings to remote RESPIRA stations via FIWARE. We explained in [this other section](RESPIRA_CALIBRATION.md) two different calibration strategies: automatic manual factor-offset correction and zero-calibration. The following sections will employ each of these techniques by means of the corresponding command.

# Manual factor-offset correction

Assuming that you already calculated your correction values (factor and offset), transmitting them to FIWARE only requires this command:

```
python3 respira_tool.py --calibrate no2 -d RESPIRA_XXXXXXXXXXXX -f 1.0021 -o -12.687
```

Where no2 is the reading to be corrected, RESPIRA_XXXXXXXXXXXX is the ID of the RESPIRA station, 1.0021 is the correction factor (or gain) and -12.687 is the correction offset. Supported pollutant by this version are: no2, pm1.0, pm2.5, pm4.0 and pm10 so we can send calibration settings for each individual gas or particulate matter.

```
python3 respira_tool.py --calibrate pm2.5 -d RESPIRA_XXXXXXXXXXXX -f 1.0016 -o 5.342
```

RESPIRA stations periodically query the FIWARE Context-Broker for new config settings every hour. Once the new settings have been retrieved, the station will start applying them for the next transmission, one hour later.

# Automatic zero-level correction

This strategy allows the station to subtract a zero-level offset to any reading. This zero-level corresponds to the minimum level detected in a 10-day interval. We can enable this functionality for both the NO2 sensor and the whole particulate matter sensor (SPS30). Please note that we can not enable zero-calibration only for a single particulate mater parameter.

These commands are used to enable automatic zero-calibration for each sensor:

```
python3 respira_tool.py --enable-zero-calibration no2 -d RESPIRA_XXXXXXXXXXXX
python3 respira_tool.py --enable-zero-calibration pm -d RESPIRA_XXXXXXXXXXXX
```

or diasble zero calibration:


```
python3 respira_tool.py --disable-zero-calibration no2 -d RESPIRA_XXXXXXXXXXXX
python3 respira_tool.py --disable-zero-calibration pm -d RESPIRA_XXXXXXXXXXXX
```

As stated before, these changes take effect starting from the next transmission, one hour later.

# Reset calibration values

Let's say that we want to revert to the default configuration values, which are:

- Automatic zero calibration disabled for both sensors
- Manual correction factor = 1 and offset = 0 for all pollutants.

We can run the following command to set the configuration to factory defaults:

```
python3 respira_tool.py --reset-calibration -d RESPIRA_XXXXXXXXXXXX
```

