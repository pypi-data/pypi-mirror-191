# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sopic', 'sopic.gui', 'sopic.utils']

package_data = \
{'': ['*']}

install_requires = \
['PyQt5>=5,<6', 'colorlog>=4,<5', 'pygraphviz==1.8']

setup_kwargs = {
    'name': 'sopic',
    'version': '0.1.1',
    'description': 'Helper for manufacturing station',
    'long_description': 'None',
    'author': "Thomas 'Taldrain' Mariaux",
    'author_email': 'taldrain@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
