# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['djplus',
 'djplus.auth',
 'djplus.auth.migrations',
 'djplus.auth.validators',
 'djplus.blog',
 'djplus.blog.migrations',
 'djplus.project_template',
 'djplus.project_template.project_name',
 'djplus.project_template.project_name.settings']

package_data = \
{'': ['*'],
 'djplus.auth': ['templates/auth/*'],
 'djplus.blog': ['templates/blog/*'],
 'djplus.project_template': ['requirements/*',
                             'static/css/*',
                             'static/js/*',
                             'templates/*']}

install_requires = \
['Django>=4.0.3,<5.0.0']

entry_points = \
{'console_scripts': ['djplus = djplus.__main__:main',
                     'djplusconfig = djplus.__main__:generate_config_file']}

setup_kwargs = {
    'name': 'jommerce',
    'version': '2.1.0',
    'description': 'More than a reusable app',
    'long_description': '![djplus version](https://img.shields.io/pypi/v/djplus?style=flat-square)\n![django version](https://img.shields.io/pypi/djversions/djplus?style=flat-square)\n![python version](https://img.shields.io/pypi/pyversions/djplus?style=flat-square)\n![license](https://img.shields.io/pypi/l/djplus?color=blue&style=flat-square)\n\n# what is djplus?\n<span style="color: white;background-color: green">Dj+</span> is **More than a reusable app** that solves 80% of the needs of any website project.\n(such as blog, store, academy, authentication, admin, contact us, about us, forum, ... etc.)\nand these apps can be customized with Django settings.\n\n# how to install?\n```shell\npip install djplus\n```\n',
    'author': 'githashem',
    'author_email': 'PersonalHashem@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/githashem/djplus',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
