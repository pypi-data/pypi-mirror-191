# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['myfr24']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.2,<5.0.0', 'requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'myfr24',
    'version': '0.1.1',
    'description': 'Simple tool to query myFlightRadar24 profiles',
    'long_description': '',
    'author': 'Franco Correa',
    'author_email': 'franco@francocorrea.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
