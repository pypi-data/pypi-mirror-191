# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bayesiannetworkx']

package_data = \
{'': ['*']}

install_requires = \
['python-semantic-release>=7.33.1,<8.0.0', 'semver>=2.13.0,<3.0.0']

setup_kwargs = {
    'name': 'bayesiannetworkx',
    'version': '0.0.3',
    'description': '',
    'long_description': '# Inteligencia Artificial: Laboratorio 2 - Inferencia Probabilistica',
    'author': 'javim7',
    'author_email': '61723252+javim7@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
