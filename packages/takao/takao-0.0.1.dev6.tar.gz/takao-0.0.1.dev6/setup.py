# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['takao']

package_data = \
{'': ['*'], 'takao': ['partials/*', 'static/*', 'static/Inter (web)/*']}

install_requires = \
['sphinx>=4']

entry_points = \
{'sphinx.html_themes': ['takao = takao']}

setup_kwargs = {
    'name': 'takao',
    'version': '0.0.1.dev6',
    'description': 'A dark theme for Sphinx.',
    'long_description': '# Takao\n\nTakao is a dark theme for the\n[Sphinx documentation generator](https://www.sphinx-doc.org).\n\nI created it mainly for my own projects. Feel free to try it and open an issue\nif you have any problems.\n\n## Licence\n\nTakao uses the MIT licence.\n\nDistributions of Takao include the [Inter font](https://github.com/rsms/inter),\nwhich\n[uses the SIL Open Font Licence](https://github.com/rsms/inter/blob/master/LICENSE.txt).\n\n## Installation\n\n1. Install the Python package:\n\n   ```shell\n   pip install takao\n   ```\n\n2. Update `html_theme` in your Sphinx project configuration:\n\n   ```python\n   html_theme = "takao"\n   ```\n\n3. Create a clean documentation build in your Sphinx project directory:\n\n   ```shell\n   make clean\n   make html\n   ```\n\n## Development\n\nDevelopment of Takao requires Python 3.11, [Poetry](https://python-poetry.org)\nand Node.js 18.\n\n### Building a wheel\n\n1. Install Python dependencies:\n\n   ```shell\n   poetry install\n   ```\n\n2. Install Node.js dependencies:\n\n   ```shell\n   npm install\n   ```\n\n3. Build static assets:\n\n   ```shell\n   npm run build\n   ```\n\n4. Build the wheel :\n   ```shell\n   poetry build\n   ```\n',
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
