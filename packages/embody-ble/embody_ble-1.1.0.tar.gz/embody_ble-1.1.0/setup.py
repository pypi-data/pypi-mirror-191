# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['embodyble']

package_data = \
{'': ['*']}

install_requires = \
['bleak>=0.19.5,<0.20.0', 'embody-serial>=1.0.11']

entry_points = \
{'console_scripts': ['embody-ble = embodyble.cli:main']}

setup_kwargs = {
    'name': 'embody-ble',
    'version': '1.1.0',
    'description': 'Communicate with the EmBody device over BLE (bluetooth)',
    'long_description': '# Embody BLE\n\n[![PyPI](https://img.shields.io/pypi/v/embody-ble.svg)][pypi_]\n[![Status](https://img.shields.io/pypi/status/embody-ble.svg)][status]\n[![Python Version](https://img.shields.io/pypi/pyversions/embody-ble)][python version]\n[![License](https://img.shields.io/pypi/l/embody-ble)][license]\n\n[![Tests](https://github.com/aidee-health/embody-ble/workflows/Tests/badge.svg)][tests]\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]\n\n[pypi_]: https://pypi.org/project/embody-ble/\n[status]: https://pypi.org/project/embody-ble/\n[python version]: https://pypi.org/project/embody-ble\n[tests]: https://github.com/aidee-health/embody-ble/actions?workflow=Tests\n[pre-commit]: https://github.com/pre-commit/pre-commit\n[black]: https://github.com/psf/black\n\n## Features\n\n- Connects to an EmBody device over BLE (Bluetooth) using [Bleak](https://github.com/hbldh/bleak)\n- Uses the EmBody protocol to communicate with the device\n- Integrates with [the EmBody Protocol Codec](https://github.com/aidee-health/embody-protocol-codec) project\n- Asynchronous send without having to wait for response\n- Synchronous send where response message is returned\n- Provides callback interfaces for incoming messages, response messages and connect/disconnect\n- Facade method to send/receive BLE messages directly\n- All methods and callbacks are threadsafe\n- Separate threads for send, receive and callback processing\n- Type safe code using [mypy](https://mypy.readthedocs.io/) for type checking\n- High level callback interface for attribute reporting\n\n## Requirements\n\n- Python 3.9-3.11\n- Access to private Aidee Health repositories on Github\n\n## Installation\n\nYou can install _Embody BLE_ via [pip]:\n\n```console\n$ pip install embody-ble\n```\n\nThis adds `embody-ble` as a library, but also provides the CLI application with the same name.\n\n## Usage\n\nA very basic example where you send a message request and get a response:\n\n```python\nfrom embodyble.embodyble import EmbodyBle\nfrom embodyserial.helpers import EmbodySendHelper\n\nembody_ble = EmbodyBle()\nsend_helper = EmbodySendHelper(sender=embody_ble)\nembody_ble.connect()\nprint(f"Serial no: {send_helper.get_serial_no()}")\nembody_ble.shutdown()\n```\n\nIf you want to see more of what happens under the hood, activate debug logging before setting up `EmbodyBle`:\n\n```python\nimport logging\n\nlogging.basicConfig(level=logging.DEBUG)\n```\n\n## Using the application from the command line\n\nThe application also provides a CLI application that is automatically added to the path when installing via pip.\n\nOnce installed with pip, type:\n\n```\nembody-ble --help\n```\n\nTo see which options are available.\n\n> **Note**\n> The serial port is automatically detected, but can be overridden by using the `--device` option.\n\n### Example - Attribute reporting\n\nTo see how attribute reporting can be configured, have a look at the example in [examples/reporting_example.py](./examples/reporting_example.py)\n\nYou can also test attribute reporting using the cli:\n\n```shell\nembody-ble --log-level INFO --report-attribute battery_level --report-interval 1\n```\n\n```shell\nembody-ble --log-level INFO --report-attribute heart_rate --report-interval 1000\n```\n\n### Example - List all available EmBody devices\n\n```shell\nembody-ble --list-devices\n```\n\n### Example - List all attribute values\n\n```shell\nembody-ble --get-all\n```\n\n### Example - Get serial no of device\n\n```shell\nembody-ble --get serialno\n```\n\n### Example - List files over serial port\n\n```shell\nembody-ble --list-files\n```\n\n### Example - Set time current time (UTC)\n\n```shell\nembody-ble --set-time\n```\n\n## Troubleshooting\n\nNo known issues registered.\n\n## Contributing\n\nContributions are very welcome.\nTo learn more, see the [Contributor Guide].\n\n## Issues\n\nIf you encounter any problems,\nplease [file an issue] along with a detailed description.\n\n[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n[file an issue]: https://github.com/aidee-health/embody-ble/issues\n[pip]: https://pip.pypa.io/\n\n<!-- github-only -->\n\n[license]: https://github.com/aidee-health/embody-ble/blob/main/LICENSE\n[contributor guide]: https://github.com/aidee-health/embody-ble/blob/main/CONTRIBUTING.md\n[command-line reference]: https://embody-ble.readthedocs.io/en/latest/usage.html\n',
    'author': 'Aidee Health AS',
    'author_email': 'hello@aidee.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/aidee-health/embody-ble',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
