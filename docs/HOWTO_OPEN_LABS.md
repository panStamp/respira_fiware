[< back to index](../README.md)

# Index of contents

- [Create account](#create-account)
- [Create device profile](#create-device-profile)

# Create account

Although _Environmental Open Labs_ can be freely viewed and browsed without the need to be registered, registered accounts can also create devices and transmit IoT data to the platform. If you got to this tutorial is probably because you want to connect your IoT device to _Environmental Open Labs_. In this case, please proceed to create an account from [here]().

Once your account is created

# Create device profile

Device profiles are type of devices with a documented set of endpoints (inputs). When you create a new device you need to associate it to a specific device profile. Thus, before creating your first device you have to define how many endpoints this device will have and how they will perform.

Let's say we want to create a device capable to transmit temperatures and humidities to the platform. We have then to create a new device profile from _Devices->Create new device profile_, then create a new endpoint for the temperature sensor and document it as follows:

Then repeat the same process for the humidity sensor:

After confirmation the system will return an API key that needs to be entered in your device. This key corresponds to the FIWARE API key for the UltraLight (UL) IoT agent. The platform will also return an example of UL frame that can be used in your code:

Example of UL frame: _t|25.00#h|40.00_

that can be translated into true source code as follows:

```C++
sprintf(txBuf, "t|%.2f#h|%.2f", temperature, humidity);
```

# Create device

Once our first device profile is created we can create a new device. Click on _Devices->Create new device_ and select the recently created device profile.

