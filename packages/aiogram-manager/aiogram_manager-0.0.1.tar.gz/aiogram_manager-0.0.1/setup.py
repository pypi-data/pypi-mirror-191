# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiogram_manager']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3', 'cookiecutter>=2.1.1', 'pydantic>=1.10.4']

entry_points = \
{'console_scripts': ['aiogram = aiogram_manager.main:cli']}

setup_kwargs = {
    'name': 'aiogram-manager',
    'version': '0.0.1',
    'description': 'Managing aiogram projects',
    'long_description': '',
    'author': 'BulatXam',
    'author_email': 'Khamdbulat@yandex.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
