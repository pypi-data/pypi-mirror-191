# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pytest_ruff']
install_requires = \
['ruff>=0.0.244,<0.0.245']

entry_points = \
{'pytest11': ['ruff = pytest_ruff']}

setup_kwargs = {
    'name': 'pytest-ruff',
    'version': '0.0.2',
    'description': 'pytest plugin to check ruff requirements.',
    'long_description': '# pytest-ruff',
    'author': 'Iuri de Silvio',
    'author_email': 'iurisilvio@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
