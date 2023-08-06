# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['trigger_count']

package_data = \
{'': ['*']}

install_requires = \
['labjack-ljm>=1.21.0,<2.0.0']

setup_kwargs = {
    'name': 'trigger-count',
    'version': '0.1.2',
    'description': '',
    'long_description': '',
    'author': 'Mathis',
    'author_email': 'mathis.bassler@protonmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
