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
    'version': '0.0.3',
    'description': 'pytest plugin to check ruff requirements.',
    'long_description': '# pytest-ruff\n\nA pytest plugin to run [ruff](https://pypi.org/project/ruff/).\n\n## Installation\n\n```shell\npip install pytest-ruff\n```\n\n## Usage\n\n```shell\npytest --ruff\n```\n\nThe plugin will run one ruff check test per file and fail if code is not ok for ruff.\n\n## Configuration\n\nYou can override ruff configuration options by placing a `pyproject.toml` or `ruff.toml` file in your project directory, like when using standalone ruff.\n\n## License\n\nDistributed under the terms of the `MIT` license, `pytest-ruff` is free and open source software.\n',
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
