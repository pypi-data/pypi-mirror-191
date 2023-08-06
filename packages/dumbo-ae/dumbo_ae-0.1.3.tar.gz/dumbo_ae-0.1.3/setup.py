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
    'version': '0.1.3',
    'description': 'CLI per il corso di Architettura degli Elaboratori',
    'long_description': "# Dumbo Architettura degli Elaboratori\n\nUna semplice interfaccia a linea di comando per il corso di Architettura degli Eleboratori.\n\n\n## Prerequisiti\n\nPython 3.10+\n\n## Installazione\n\nIl modo più semplice è usare pip:\n\n```bash\n$ pip3 install dumbo-ae\n```\n\n\n## Uso\n\nPer controllare la propria soluzione a un esercizio è necessario indicare l'UUID dell'esercizio (fornito in aula) e il file sorgente della propria soluzione: \n```bash\n$ python3 -m dumbo_ae checker --of <UUID> <file-sorgente>\n```\n",
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
