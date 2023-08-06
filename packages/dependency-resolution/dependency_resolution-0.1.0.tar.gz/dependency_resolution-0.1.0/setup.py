# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dependency_resolution']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'dependency-resolution',
    'version': '0.1.0',
    'description': 'A simple dependency resolution library using container concepts',
    'long_description': 'None',
    'author': 'Saroopashree K',
    'author_email': 'saroopa25@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10.0,<3.11.0',
}


setup(**setup_kwargs)
