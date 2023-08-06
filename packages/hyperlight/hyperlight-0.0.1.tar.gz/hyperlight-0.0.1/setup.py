# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hyperlight', 'hyperlight.hyper', 'hyperlight.nn']

package_data = \
{'': ['*']}

install_requires = \
['pyyaml>=6.0,<7.0']

setup_kwargs = {
    'name': 'hyperlight',
    'version': '0.0.1',
    'description': '',
    'long_description': '',
    'author': 'Jose Javier',
    'author_email': '3844846+JJGO@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
