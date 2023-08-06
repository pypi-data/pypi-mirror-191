# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ooler_ble_client']

package_data = \
{'': ['*']}

install_requires = \
['bleak-retry-connector>=2.3.0', 'bleak>=0.19.0']

setup_kwargs = {
    'name': 'ooler-ble-client',
    'version': '0.1.1',
    'description': 'A library to communicate with Ooler Sleep System Bluetooth devices.',
    'long_description': '# ooler_ble_client\nA library to communicate with Ooler Sleep System Bluetooth devices.',
    'author': 'Robby Griffin',
    'author_email': 'rgriffin@postlogical.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/PostLogical/ooler_ble_client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
