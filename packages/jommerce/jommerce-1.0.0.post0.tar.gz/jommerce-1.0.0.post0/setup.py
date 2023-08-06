# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['djplus',
 'djplus.project_template',
 'djplus.project_template.project_name',
 'djplus.project_template.project_name.settings']

package_data = \
{'': ['*']}

install_requires = \
['Django>=4.0.3,<5.0.0']

entry_points = \
{'console_scripts': ['djplus = djplus.__main__:main']}

setup_kwargs = {
    'name': 'jommerce',
    'version': '1.0.0.post0',
    'description': 'django ready apps',
    'long_description': '# djplus',
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
