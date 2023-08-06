# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['takao']

package_data = \
{'': ['*'], 'takao': ['partials/*']}

install_requires = \
['sphinx>=4']

entry_points = \
{'sphinx.html_themes': ['takao = takao']}

setup_kwargs = {
    'name': 'takao',
    'version': '0.0.1.dev0',
    'description': 'A dark theme for Sphinx.',
    'long_description': '# Takao\n\nTakao is a dark theme for Sphinx I created for use in my own projects.\n\n## Installation\n\n1. Install the Python package:\n\n   ```shell\n   pip install takao\n   ```\n\n2. Update `html_theme` in your Sphinx project configuration:\n\n   ```python\n   html_theme = "takao"\n   ```\n\n3. Create a fresh documentation build in your Sphinx project directory:\n\n   ```shell\n   make clean\n   make html\n   ```\n',
    'author': 'Reupen Shah',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/reupen/takao',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
