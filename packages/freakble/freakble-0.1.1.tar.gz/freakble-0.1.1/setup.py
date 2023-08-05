# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['freakble']

package_data = \
{'': ['*']}

install_requires = \
['ble-serial>=2.7.0,<3.0.0', 'click>=8.1.3,<9.0.0']

entry_points = \
{'console_scripts': ['freakble = freakble.main:run']}

setup_kwargs = {
    'name': 'freakble',
    'version': '0.1.1',
    'description': 'A simple tool to send messages into FreakWAN over Bluetooth low energy.',
    'long_description': "# freakble\n\nA simple tool to send messages into [FreakWAN](https://github.com/antirez/sx1276-micropython-driver/)\nover Bluetooth low energy.\n\n**This is still a work in progress and it's not complete.**\n\n## Installation\n\n### Using pipx\n\nThe best way to install freakble is using [pipx](https://pypa.github.io/pipx/):\n```console\n$ pipx install freakble\n```\n\n### Using pip\n\n```console\n$ python -m pip install freakble\n```\n\n### From source\n\nfreakble uses [Poetry](https://python-poetry.org) as dependency management and\npackaging tool, you need to install it first.\n\nThen:\n\n1. Clone this repository.\n2. From the root of the repository run:\n   ```console\n   $ poetry build\n   ```\n3. Install using pipx or pip (it's better to use pipx):\n   ```console\n   $ pipx install dist/freakble-0.1.0-py3-none-any.whl\n   ```\n\n## Usage\n\nAt the moment only the command `send` used to send a message to the board is\nimplemented. You need to already know the address of the device.\n\nFor example:\n\n```console\n$ freakble send --device AA:AA:AA:AA:AA:AA Hello, there!\n```\n\nwhere you have to substitute `AA:AA:AA:AA:AA:AA` with your device's address.\n\nThe `--loop` flag will make freakble to send continuosly the message until\n`CTRL + C` is pressed. Right now the resend interval is hardcoded and its value\nis 0.1 seconds.\n\n```console\n$ freakble send --device AA:AA:AA:AA:AA:AA --loop FREAKNET\n```\n\n![A photo of a LYLIGO TTGO LoRa v2 1.6 showing the text: you> FREAKNET in multiple lines.](extras/304f4bb6-4f51-4183-95b9-c329b9bf69ab.jpg)\n",
    'author': 'Daniele Tricoli',
    'author_email': 'eriol@mornie.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://noa.mornie.org/eriol/freakble',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
