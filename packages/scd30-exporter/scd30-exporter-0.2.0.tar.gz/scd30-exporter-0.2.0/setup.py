# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['scd30_exporter']

package_data = \
{'': ['*']}

install_requires = \
['adafruit-circuitpython-scd30>=2.2.9,<3.0.0',
 'prometheus-client>=0.16.0,<0.17.0']

entry_points = \
{'console_scripts': ['scd30-exporter = scd30_exporter.cli:main']}

setup_kwargs = {
    'name': 'scd30-exporter',
    'version': '0.2.0',
    'description': 'Prometheus exporter for Adafruit SCD-30 - NDIR CO2 Temperature and Humidity Sensor',
    'long_description': '# scd30-exporter\n\nPrometheus exporter for Adafruit SCD-30 - NDIR CO2 Temperature and Humidity Sensor.\n\n\n## Installing\n\n```sh\npip3 install scd30-exporter\n```\n\n## Running\n\n```sh\nscd30-exporter --port 8000 --interval 10\n```\n\n\n## Developing\n\nSee [DEVELOPING.md](DEVELOPING.md)\n',
    'author': 'Sergej Alikov',
    'author_email': 'sergej@alikov.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/node13h/scd30-exporter',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
