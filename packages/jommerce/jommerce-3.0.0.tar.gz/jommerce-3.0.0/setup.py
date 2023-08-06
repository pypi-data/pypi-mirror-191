# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jommerce',
 'jommerce.auth',
 'jommerce.auth.migrations',
 'jommerce.auth.validators',
 'jommerce.blog',
 'jommerce.blog.migrations',
 'jommerce.project',
 'jommerce.project.settings',
 'jommerce.project_template',
 'jommerce.project_template.project_name',
 'jommerce.project_template.project_name.settings']

package_data = \
{'': ['*'],
 'jommerce.auth': ['templates/auth/*'],
 'jommerce.blog': ['templates/blog/*'],
 'jommerce.project': ['static/css/*', 'static/js/*', 'templates/*'],
 'jommerce.project_template': ['requirements/*',
                               'static/css/*',
                               'static/js/*',
                               'templates/*']}

install_requires = \
['Django>=4.0.3,<5.0.0', 'django-ipware>=4.0.2,<5.0.0']

entry_points = \
{'console_scripts': ['jecret = jommerce.__main__:get_random_secret_key',
                     'jommerce = jommerce.__main__:main',
                     'jonfig = jommerce.__main__:generate_config_file']}

setup_kwargs = {
    'name': 'jommerce',
    'version': '3.0.0',
    'description': 'A collection of Django apps',
    'long_description': '![jommerce version](https://img.shields.io/pypi/v/jommerce?style=flat-square)\n![django version](https://img.shields.io/pypi/djversions/jommerce?style=flat-square)\n![python version](https://img.shields.io/pypi/pyversions/jommerce?style=flat-square)\n![license](https://img.shields.io/pypi/l/jommerce?color=blue&style=flat-square)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n# Why does this package exist?\nBecause 80% of customer projects have common apps \nsuch as authentication, store, admin, blog, forum, academy, etc. \nTherefore, as freelancers, we decided to code all these apps only once in one place \nand use them in different projects as often as desired, \nand all these apps can be customized by the settings of each project.\nThis helps to save our time and increase our income in exchange for doing projects.\n\n# Installing\nYou can use pip to install `jommerce` for usage:\n```shell\npip install jommerce\n```\n\n# Usage\n## Create Project\nSimple command line for jumpstarting production-ready Django projects:\n```shell\njommerce\n```\nor\n```shell\npython -m jommerce\n```\n\n## Auth\n\n```python\n#settings.py\n\nINSTALLED_APPS = [\n    # ...\n    "jommerce.auth", \n    # ...\n]\n\nMIDDLEWARE = [\n    # ...\n    \'jommerce.auth.middleware.AuthenticationMiddleware\',\n    # ...\n]\n```\n```python\n# urls.py\nfrom django.urls import path, include\n\nurlpatterns = [\n    # ...\n    path("auth/", include("jommerce.auth.urls", namespace="auth")),\n    # ...\n]\n```\n## Blog\n\n```python\n#settings.py\n\nINSTALLED_APPS = [\n    # ...\n    "jommerce.blog", \n    # ...\n]\n```\n```python\n# urls.py \nfrom django.urls import path, include\n\nurlpatterns = [\n    # ...\n    path("blog/", include("jommerce.blog.urls", namespace="blog")),\n    # ...\n]\n```\n# Contributing\nContributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.\n\nIf you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".\nDon\'t forget to give the project a star! Thanks again!\n\n1. Fork the Project\n2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)\n3. Commit your Changes (`git commit -m \'Add some AmazingFeature\'`)\n4. Push to the Branch (`git push origin feature/AmazingFeature`)\n5. Open a Pull Request\n',
    'author': 'githashem',
    'author_email': 'PersonalHashem@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/jommerce/jommerce',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
