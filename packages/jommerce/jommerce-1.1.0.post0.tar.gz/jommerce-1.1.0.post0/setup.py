# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['djplus',
 'djplus.auth',
 'djplus.auth.migrations',
 'djplus.auth.validators',
 'djplus.project_template',
 'djplus.project_template.project_name',
 'djplus.project_template.project_name.settings']

package_data = \
{'': ['*'],
 'djplus.auth': ['templates/auth/*'],
 'djplus.project_template': ['static/css/*', 'static/js/*', 'templates/*']}

install_requires = \
['Django>=4.0.3,<5.0.0']

extras_require = \
{'argon2': ['argon2-cffi>=21.3.0,<22.0.0'], 'bcrypt': ['bcrypt>=3.2.2,<4.0.0']}

entry_points = \
{'console_scripts': ['djplus = djplus.__main__:main']}

setup_kwargs = {
    'name': 'jommerce',
    'version': '1.1.0.post0',
    'description': 'django ready apps',
    'long_description': '<br /> \n<div align="center">\n  <a href="https://github.com/githashem/djplus">\n    <img src="https://raw.githubusercontent.com/githashem/djplus/main/logo.svg" alt="Djplus Logo" width="80" height="80">\n  </a>\n<h2 align="center">A package of ready-made apps</h2>\n</div>\n\n![djplus version](https://img.shields.io/pypi/v/djplus?style=flat-square)\n',
    'author': 'githashem',
    'author_email': 'PersonalHashem@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/githashem/djplus',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
