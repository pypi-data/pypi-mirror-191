# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['beholder_client']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.2.0,<10.0.0', 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'beholder-client',
    'version': '0.1.0',
    'description': 'Python client library for beholder.',
    'long_description': '# beholder-py\n\nPython client library for [beholder](https://github.com/mbari-org/beholder).\n\n## Build\n\nThis project is built with [Poetry](https://python-poetry.org/).\n\nYou can build the project with the following command:\n\n```bash\npoetry build\n```\n\nThis will create a `dist/` directory with the built `beholder` package.\n\n## Install\n\nYou can install the built package with the following command:\n\n```bash\npip install dist/beholder-<VERSION>.whl\n```\n\n## Development\n\nTo configure the project for development, install Poetry and run\n\n```bash\npoetry install\npoetry shell\n```\n\nThis will create a virtual environment for the project, install all dependencies into it, then spawn a new shell with the environment activated.\n\n---\n\n&copy; Monterey Bay Aquarium Research Institute, 2022',
    'author': 'Kevin Barnard',
    'author_email': 'kbarnard@mbari.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mbari-org/beholder-py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
