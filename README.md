# Daikin Residential Controller homeassistant integration
Cloud control of Daikin devices that are supported by Daikin Residential Controller app. When you want to control a Daikin Altherma you can't use this integration but use the [daikin_residential_altherma](https://github.com/speleolontra/daikin_residential_altherma) or [daikin_residential_brp069a62](https://github.com/BigFoot2020/daikin_residential_brp069a62) integration.

# Compatibility

This integration is verified to be compatible with the following Daikin adapters (usually integrated in the device):
- BRP069C4x

# Installation:

Copy the daikin_residential folder and all of its contents into your Home Assistant's custom_components folder. This is often located inside of your /config folder. If you are running Hass.io, use SAMBA to copy the folder over. If you are running Home Assistant Supervised, the custom_components folder might be located at /usr/share/hassio/homeassistant. It is possible that your custom_components folder does not exist. If that is the case, create the folder in the proper location, and then copy the daikin_residential folder and all of its contents inside the newly created custom_components folder.

Alternatively, you can install daikin_residential through HACS by adding this repository.

# Usage:

**NOTE: since v.2.0.x, the tokenset.json file is no longer needed because the integration can connect and retrieve the tokens autonomously. When installing v.2.0.x from a previous one, the integration must be deleted and re-added.**

The integration can be configured in two ways:

# 1. YAML config files

Just add the following lines to your configuration.yaml file specifying the email and password used in the Daikin Residential App, and the Daikin devices connected to your cloud account will be created.

```
daikin_residential:
  email: [your_email]
  password: [your_pwd]

```


# 2. Using config flow

Start by going to Configuration - Integration and pressing the "+ ADD INTEGRATION" button to create a new Integration, then select Daikin Residential Controller in the drop-down menu.

Follow the instructions, you just have to type the email and password used in the Daikin Residential App. After pressing the "Submit" button, the integration will be added, and the Daikin devices connected to your cloud account will be created.


# To-do list:

* Fix spurious glitches.
* Maybe improve the sensors for Energy consumption.

# Thanks to:

This code is based on @Apollon77 's great work, in finding a way to retrieve the token set, and to send the HTTP commands over the cloud. This integration would not exist without his precious job, my job was just to find a way to port his code from nodeJS to python, and then create the integration.

<a href="https://www.buymeacoffee.com/rospogrigio" target="_blank"><img src="https://bmc-cdn.nyc3.digitaloceanspaces.com/BMC-button-images/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;" ></a>
<a href="https://paypal.me/rospogrigio" target="_blank"><img src="https://www.paypalobjects.com/webstatic/mktg/logo/pp_cc_mark_37x23.jpg" border="0" alt="PayPal Logo" style="height: auto !important;width: auto !important;"></a>
