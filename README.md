# Daikin Residential Controller homeassistant integration
Cloud control of Daikin devices that are supported by Daikin Residential Controller app.

# Installation:

Copy the daikin_residential folder and all of its contents into your Home Assistant's custom_components folder. This is often located inside of your /config folder. If you are running Hass.io, use SAMBA to copy the folder over. If you are running Home Assistant Supervised, the custom_components folder might be located at /usr/share/hassio/homeassistant. It is possible that your custom_components folder does not exist. If that is the case, create the folder in the proper location, and then copy the daikin_residential folder and all of its contents inside the newly created custom_components folder.

Alternatively, you can install daikin_residential through HACS by adding this repository.

# Usage:

**NOTE: You must have your Daikin Cloud token set stored as a tokenset.json file in your /config folder (the same where configuration.yaml is). For instructions on how to retrieve this file, follow the guide at https://github.com/Apollon77/daikin-controller-cloud/blob/main/PROXY.md .**

The integration can be configured in two ways:

# 1. YAML config files

Just add the following line to your configuration.yaml file, and the Daikin devices connected to your cloud account will be created.

```
daikin_residential:
```


# 2. Using config flow

Start by going to Configuration - Integration and pressing the "+" button to create a new Integration, then select Daikin Residential Controller in the drop-down menu.


# To-do list:

* Fix spurious glitches.
* Maybe improve the sensors for Energy consumption.

# Thanks to:

This code is based on @Apollon77 's great work, in finding a way to retrieve the token set, and to send the HTTP commands over the cloud. This integration would not exist without his precious job.
