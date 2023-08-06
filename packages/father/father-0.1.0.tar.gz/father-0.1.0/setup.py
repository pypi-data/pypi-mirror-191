# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['father']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'father',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'githashem',
    'author_email': 'PersonalHashem@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
