[![](https://img.shields.io/github/release/rospogrigio/daikin_residential/all.svg?style=for-the-badge)](https://github.com/rospogrigio/daikin_residential/releases)
[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)
[![](https://img.shields.io/badge/MAINTAINER-%40rospogrigio-green?style=for-the-badge)](https://github.com/rospogrigio)


# Daikin Residential Controller (ONECTA) homeassistant integration
Cloud control of Daikin devices that are supported by Daikin Residential Controller (now "ONECTA - Daikin") app.

> [!IMPORTANT]
> This integration is no longer working since March 16th 2024 due to changes made by Daikin (see [https://github.com/rospogrigio/daikin_residential/issues/204](https://github.com/rospogrigio/daikin_residential/issues/182#issuecomment-1933967548)). Please migrate to the [daikin_onecta](https://github.com/jwillemsen/daikin_onecta) integration which supports the Daikin AC units but also other types of Daikin devices, such as the Daikin Altherma heat pumps. 

# Thanks to:

This code is based on @Apollon77 's great work, in finding a way to retrieve the token set, and to send the HTTP commands over the cloud. This integration would not exist without his precious job, my job was just to find a way to port his code from nodeJS to python, and then create the integration.

Other thanks go to @jwillemsen for support and suggestions for this Integration, and for developing the new Integration that merges the changes for the Altherma heat pumps and incorporates the new authentication requested by Daikin.

<a href="https://www.buymeacoffee.com/rospogrigio" target="_blank"><img src="https://bmc-cdn.nyc3.digitaloceanspaces.com/BMC-button-images/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;" ></a>
<a href="https://paypal.me/rospogrigio" target="_blank"><img src="https://www.paypalobjects.com/webstatic/mktg/logo/pp_cc_mark_37x23.jpg" border="0" alt="PayPal Logo" style="height: auto !important;width: auto !important;"></a>
