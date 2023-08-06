# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['airton_ac', 'airton_ac.domoticz']

package_data = \
{'': ['*']}

install_requires = \
['local-tuya>=1.2.2,<2']

setup_kwargs = {
    'name': 'airton-ac',
    'version': '2.0.0',
    'description': 'Control an Airton AC device over LAN.',
    'long_description': '# airton-ac\n\n[![tests](https://github.com/gpajot/airton-ac/workflows/Test/badge.svg?branch=main&event=push)](https://github.com/gpajot/airton-ac/actions?query=workflow%3ATest+branch%3Amain+event%3Apush)\n[![version](https://img.shields.io/pypi/v/airton-ac?label=stable)](https://pypi.org/project/airton-ac/)\n[![python](https://img.shields.io/pypi/pyversions/airton-ac)](https://pypi.org/project/airton-ac/)\n\nControl an Airton AC device over LAN.\nThis requires having the [wifi module](https://eu.airton.shop/en/products/kit-module-wifi-pour-climatiseurs-airton-en-wifi-ready).\n\n## Features\n- asynchronous methods and transport\n- persistent communication to the device\n- automatic remote device state updates (remotes can still be used)\n- configurable buffering for subsequent updates\n- constraints between device commands\n- Domoticz plugin using a dedicated thread\n\n## Usage\nSee [local tuya requirements](https://github.com/gpajot/local-tuya#requirements) first to find device information.\n\nExample usage:\n```python\nfrom local_tuya import DeviceConfig, ProtocolConfig\nfrom airton_ac import ACDevice, ACFanSpeed\n\n\nasync with ACDevice(DeviceConfig(ProtocolConfig("{id}", "{address}", b"{key}"))) as device:\n    await device.switch(True)\n    await device.set_speed(ACFanSpeed.L2)\n    await device.switch(False)\n```\n\n## Domoticz plugin\nThe plugin requires having fetched device information using instructions above.\nMake sure to read [plugin instructions](https://www.domoticz.com/wiki/Using_Python_plugins) first.\n> 💡 The Domoticz version should be `2022.1` or higher.\n\n```shell\npython -m pip install --upgrade airton-ac\npython -m airton_ac.domoticz.install\n```\nDomoticz path defaults to `~/domoticz` but you can pass a `-p` option to the second command to change that:\n```shell\npython -m airton_ac.domoticz.install -p /some/other/path\n```\n\nRestart Domoticz and create a new Hardware using `Tuya Airton AC`. Fill in device information and add.\nThe hardware will create up to 5 devices to control the fan (all prefixed with hardware name):\n- `power`: to turn on or off\n- `set point`: to set the target temperature\n- `temperature`: to record curent temperature as measured by the unit\n- `mode`: to control operating mode\n- `fan`: to control fan speed\n- `eco`: toggle low heat when heating and eco-mode when cooling\n- `light`: toggle display on the unit\n- `swing`: toggle swing mode\n- `sleep`: toggle sleep mode\n- `health`: toggle health mode\n\nYou can customize the devices you want added in the hardware page.\n\nAll device names and levels can be changed once added as only IDs are used internally.\n\n',
    'author': 'Gabriel Pajot',
    'author_email': 'gab@les-cactus.co',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/gpajot/airton-ac',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.12',
}


setup(**setup_kwargs)
