# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['djplus']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'jommerce',
    'version': '0.1.0.post0',
    'description': '',
    'long_description': 'None',
    'author': 'githashem',
    'author_email': 'PersonalHashem@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
