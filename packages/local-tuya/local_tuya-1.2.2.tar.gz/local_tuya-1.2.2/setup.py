# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['local_tuya',
 'local_tuya.device',
 'local_tuya.domoticz',
 'local_tuya.domoticz.plugin',
 'local_tuya.domoticz.units',
 'local_tuya.protocol',
 'local_tuya.protocol.message',
 'local_tuya.protocol.message.handlers']

package_data = \
{'': ['*']}

install_requires = \
['concurrent-tasks>=1.3,<2', 'pycryptodomex>=3,<4', 'xmltodict>=0.13,<0.14']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=4,<5']}

setup_kwargs = {
    'name': 'local-tuya',
    'version': '1.2.2',
    'description': 'Interface to Tuya devices over LAN.',
    'long_description': "# local-tuya\n\n[![tests](https://github.com/gpajot/local-tuya/workflows/Test/badge.svg?branch=main&event=push)](https://github.com/gpajot/local-tuya/actions?query=workflow%3ATest+branch%3Amain+event%3Apush)\n[![version](https://img.shields.io/pypi/v/local-tuya?label=stable)](https://pypi.org/project/local-tuya/)\n[![python](https://img.shields.io/pypi/pyversions/local-tuya)](https://pypi.org/project/local-tuya/)\n\nInterface to Tuya devices over LAN.\n\nFeatures:\n- asynchronous methods and transport\n- persistent communication to the device\n- automatic remote device state updates (remotes can still be used)\n- configuratble of buffering for subsequent updates\n- constraints between device commands\n- Domoticz plugin using a dedicated thread\n\n> 💡 For now, only v3.3 is supported as I only own devices using this version.\n\n## Requirements\nTo control a device you will need these 3 things:\n- the device ID\n- the device local IP address\n- the device local key (encryption key generated upon pairing)\n\n> ⚠️ This library does not provide support for getting these.\n> See how to do that using any of those projects:\n> - [tuyapi](https://github.com/codetheweb/tuyapi)\n> - [tinytuya](https://github.com/jasonacox/tinytuya)\n> \n> Generous thanks to the maintainers of those tools for details on interfacing with Tuya devices.\n\n> ⚠️ Keep in mind that:\n> - After pairing the devices, it's recommended to assign static IPs in your router.\n> - If you reset or re-pair devices the local key will change.\n> - You can delete your tuya IOT account but not the SmartLife one and devices should be kept there.\n> - For state updates to be received properly, the device needs to be able to access the Tuya backend.\n\n## Architecture\nThis library is composed of two main components:\n- the Tuya protocol\n- the device\n\n### Protocol\nThe protocol is responsible for handling communication details with the Tuya device.\nIts interface consists of an asynchronous method to update the device and accepts a callback to subscribe to state changes.\n\nSee [protocol module](./local_tuya/protocol).\n\n### Device\nThe device handles higher level functional logic such as buffering, constraints and specific device commands.\n\nSee [device module](./local_tuya/device).\n\n## Domoticz plugin tools\nSee [Domoticz module](./local_tuya/domoticz).\n",
    'author': 'Gabriel Pajot',
    'author_email': 'gab@les-cactus.co',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/gpajot/local-tuya',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<3.12',
}


setup(**setup_kwargs)
