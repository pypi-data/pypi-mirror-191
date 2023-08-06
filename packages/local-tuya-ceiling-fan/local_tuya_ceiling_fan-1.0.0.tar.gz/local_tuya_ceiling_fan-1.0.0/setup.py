# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['local_tuya_ceiling_fan', 'local_tuya_ceiling_fan.domoticz']

package_data = \
{'': ['*']}

install_requires = \
['local-tuya>=1,<2']

setup_kwargs = {
    'name': 'local-tuya-ceiling-fan',
    'version': '1.0.0',
    'description': 'Control a Tuya Ceiling fan over LAN.',
    'long_description': '# local-tuya-ceiling-fan\nControl a Tuya Ceiling fan over LAN.\n\n## Usage\nSee [local tuya requirements](https://github.com/gpajot/local-tuya#requirements) first to find device information.\n\nExample usage:\n```python\nfrom local_tuya import DeviceConfig, ProtocolConfig\nfrom local_tuya_ceiling_fan import FanDevice, FanSpeed\n\n\nasync with FanDevice(DeviceConfig(ProtocolConfig("{id}", "{address}", b"{key}"))) as device:\n    await device.switch(True)\n    await device.set_speed(FanSpeed.L2)\n    await device.switch(False)\n```\n\n> 💡 There is a safety mechanism that turns off the fan and waits 30s before changing the direction.\n\n## Domoticz plugin\nThe plugin requires having fetched device information using instructions above.\nMake sure to read [plugin instructions](https://www.domoticz.com/wiki/Using_Python_plugins) first.\n> 💡 The Domoticz version should be `2022.1` or higher.\n\n```shell\npython -m pip install local-tuya-ceiling-fan\npython -m local_tuya_ceiling_fan.domoticz.install\n```\nDomoticz path defaults to `~/domoticz` but you can pass a `-p` option to the second command to change that:\n```shell\npython -m local_tuya_ceiling_fan.domoticz.install -p /some/other/path\n```\n\nRestart Domoticz and create a new Hardware using `Tuya Ceiling Fan`. Fill in device information and add.\nThe hardware will create up to 5 devices to control the fan (all prefixed with hardware name):\n- `power`: turn the fan on or off\n- `speed`: set the speed\n- `direction`: set direction\n- `light`: turn the light on or off\n- `mode`: set the operating mode\n\nYou can customize the devices you want added in the hardware page.\n\nAll device names and levels can be changed once added as only IDs are used internally.\n',
    'author': 'Gabriel Pajot',
    'author_email': 'gab@les-cactus.co',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/gpajot/local-tuya-ceiling-fan',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.12',
}


setup(**setup_kwargs)
