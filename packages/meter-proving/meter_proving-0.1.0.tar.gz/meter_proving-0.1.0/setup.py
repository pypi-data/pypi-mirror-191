# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['meter_proving']

package_data = \
{'': ['*']}

install_requires = \
['numba>=0.56.4,<0.57.0']

setup_kwargs = {
    'name': 'meter-proving',
    'version': '0.1.0',
    'description': 'library to calculate random uncertanity of a measurment sequence',
    'long_description': '',
    'author': 'StigHaraldGustavsen',
    'author_email': 'stighg@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
