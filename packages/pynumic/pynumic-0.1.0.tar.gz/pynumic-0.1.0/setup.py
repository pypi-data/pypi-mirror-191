# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pynumic']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pynumic',
    'version': '0.1.0',
    'description': 'Simple Neural Network Library',
    'long_description': '# pynumic\n\n    under construction\n\nSimple neural network library for python.\n',
    'author': 'Oleg Alexandrov',
    'author_email': 'alexandrovoleg.ru@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://zigenzoog.github.io/pynumic',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
