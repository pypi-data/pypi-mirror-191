# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiogram_manager',
 'aiogram_manager.templates',
 'aiogram_manager.templates.app',
 'aiogram_manager.templates.app.{{ cookiecutter.app_name }}',
 'aiogram_manager.templates.project',
 'aiogram_manager.templates.project.{{ cookiecutter.project_name }}',
 'aiogram_manager.templates.project.{{ cookiecutter.project_name }}.src',
 'aiogram_manager.templates.project.{{ cookiecutter.project_name }}.src.apps',
 'aiogram_manager.templates.project.{{ cookiecutter.project_name '
 '}}.src.apps.main',
 'aiogram_manager.templates.project.{{ cookiecutter.project_name }}.src.core',
 'aiogram_manager.templates.project.{{ cookiecutter.project_name '
 '}}.src.core.models']

package_data = \
{'': ['*']}

install_requires = \
['aiogram>=3.0.0b',
 'click>=8.1.3',
 'cookiecutter>=2.1.1',
 'loguru>=0.6.0',
 'pydantic>=1.10.4']

entry_points = \
{'console_scripts': ['aiogram = aiogram_manager.app:cli']}

setup_kwargs = {
    'name': 'aiogram-manager',
    'version': '1.0.0',
    'description': 'Managing aiogram projects',
    'long_description': '# aiogram-manager',
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
