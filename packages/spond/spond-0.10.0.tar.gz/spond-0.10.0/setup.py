# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spond']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.3,<4.0.0']

setup_kwargs = {
    'name': 'spond',
    'version': '0.10.0',
    'description': 'Simple, unofficial library with some example scripts to access data from the Spond API.',
    'long_description': 'None',
    'author': 'Ola Thoresen',
    'author_email': 'ola@nytt.no',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
