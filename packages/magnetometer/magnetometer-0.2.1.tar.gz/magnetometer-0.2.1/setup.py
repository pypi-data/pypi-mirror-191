# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['magnetometer',
 'magnetometer.dependencies.main.adafruit_bus_device',
 'magnetometer.dependencies.main.adafruit_lis2mdl',
 'magnetometer.dependencies.main.adafruit_lis3mdl',
 'magnetometer.dependencies.main.adafruit_mmc56x3',
 'magnetometer.dependencies.main.adafruit_register',
 'magnetometer.dependencies.main.adafruit_tlv493d',
 'magnetometer.sensors']

package_data = \
{'': ['*']}

install_requires = \
['autoregistry>=0.8,<0.9',
 'belay>=0.17.0,<0.18.0',
 'textual>=0.1.18,<0.2.0',
 'typer[all]>=0.6,<0.7']

entry_points = \
{'console_scripts': ['magnetometer = magnetometer.main:app']}

setup_kwargs = {
    'name': 'magnetometer',
    'version': '0.2.1',
    'description': '',
    'long_description': '# Magnetometer\n\nThis is a [magnetometer](https://en.wikipedia.org/wiki/Magnetometer) command-line tool that reads from physical magnetic sensors via\n[Belay](https://github.com/BrianPugh/belay).\n\n<p align="center">\n  <img width="600" src="https://user-images.githubusercontent.com/14318576/187823929-9b6985e7-4124-49b1-9e13-6268ee155d92.gif">\n</p>\n\n# Installation\nInstall Magnetometer through pip:\n\n```\npip install magnetometer\n```\n\n# Usage\n\nTo start the program, invoke `magnetometer` along with the port your\nCircuitPython board is connected to.\n\n```\nmagnetometer DEVICE_PORT --sensor SENSOR_TYPE\n```\n\nYou can use the debugging sensor `sin` without any physical hardware interactions.\nCircuitPython must be installed on-device and [must be configured with rw storage](https://belay.readthedocs.io/en/latest/CircuitPython.html).\nMagnetometer will automatically upload all necessary code to device.\nRun `magnetometer --help` to see more options.\n\n<p align="center">\n  <img width="600" src="https://user-images.githubusercontent.com/14318576/187825892-6e9594ec-9598-4aaa-9b00-fec3f82ae278.jpeg">\n</p>\n\n### Supported Sensors\n\n* [LIS3MDL](https://www.adafruit.com/product/4479) - Up to ±1,600μT\n* [MMC5603](https://www.adafruit.com/product/5579) - Up to ±3,000μT\n* [LIS2MDL](https://www.adafruit.com/product/4488) - Up to ±5,000μT\n* [TLV493D](https://www.adafruit.com/product/4366) - Up to ±130,000μT\n\nWant to support another sensor? Open an issue (or even a PR) on Github and we\ncan try to add it!\n\n# Acknowledgements\nThis tool uses many awesome libraries that keep the implementation terse and the outputs beautiful:\n* [Belay](https://github.com/BrianPugh/belay) - Seameless python/hardware interactions. Used for all hardware interactions.\n* [AutoRegistry](https://github.com/BrianPugh/autoregistry) - Automatic registry design-pattern library for mapping names to functionality. Used to manage sensor hardware abstraction layer.\n* [Textual](https://github.com/Textualize/textual) - Text User Interface framework for Python inspired by modern web development. Used for dynamic user input.\n* [Rich](https://github.com/Textualize/rich) - Python library for rich text and beautiful formatting in the terminal. Used for general UI text rendering.\n* [AsciiChartPy](https://github.com/kroitor/asciichart) - Nice-looking lightweight console ASCII line charts. Used for chart plotting. Modified to be `rich`-compatible.\n* [CircuitPython Bundle](https://github.com/adafruit/Adafruit_CircuitPython_Bundle) - A bundle of useful CircuitPython libraries ready to use from the filesystem.\n',
    'author': 'Brian Pugh',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/BrianPugh/magnetometer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
