# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dumbo_ae']

package_data = \
{'': ['*']}

install_requires = \
['dumbo-utils>=0.1.6,<0.2.0', 'requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'dumbo-ae',
    'version': '0.1.1',
    'description': 'CLI per il corso di Architettura degli Elaboratori',
    'long_description': '# Dumbo Architettura degli Elaboratori\n',
    'author': 'Mario Alviano',
    'author_email': 'mario.alviano@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
