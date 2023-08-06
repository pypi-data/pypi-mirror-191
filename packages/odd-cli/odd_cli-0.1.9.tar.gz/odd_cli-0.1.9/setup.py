# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['odd_cli', 'odd_cli.reader', 'odd_cli.reader.mapper', 'odd_cli.reader.models']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.6.0,<0.7.0',
 'odd-models>=2.0.10,<3.0.0',
 'oddrn-generator>=0.1.62,<0.2.0',
 'pyarrow>=10.0.1,<11.0.0',
 'tqdm>=4.64.1,<5.0.0',
 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['odd = odd_cli.main:app']}

setup_kwargs = {
    'name': 'odd-cli',
    'version': '0.1.9',
    'description': 'Command line tool for working with OpenDataDiscovery. ',
    'long_description': "## OpenDataDiscovery CLI\n[![PyPI version](https://badge.fury.io/py/odd-cli.svg)](https://badge.fury.io/py/odd-cli)\n\nCommand line tool for working with OpenDataDiscovery. \nIt makes it easy to create token though console and ingest local dataset's metadata to OpenDataDiscovery platform.\n\n\n#### Available commands\n```text\n╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────╮\n│ --install-completion          Install completion for the current shell.                                              │\n│ --show-completion             Show completion for the current shell, to copy it or customize the installation        │\n╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯\n╭─ Commands ─────────────────────────────────────────────────────────────────────────────────╮\n│ collect                       Collect and ingest metadata for local files from folder      │\n│ tokens                        Manipulate OpenDataDiscovery platform's tokens               │\n╰────────────────────────────────────────────────────────────────────────────────────────────╯\n```",
    'author': 'Pavel Makarichev',
    'author_email': 'vixtir90@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
