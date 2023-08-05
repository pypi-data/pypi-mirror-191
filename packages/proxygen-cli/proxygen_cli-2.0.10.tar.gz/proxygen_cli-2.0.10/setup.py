# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['proxygen_cli', 'proxygen_cli.cli', 'proxygen_cli.lib']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'cryptography>=36.0.1,<37.0.0',
 'lxml>=4.7.1,<5.0.0',
 'pydantic>=1.9.1,<2.0.0',
 'pyjwt>=2.3.0,<3.0.0',
 'pyyaml>=6.0,<7.0',
 'requests>=2.27.1,<3.0.0',
 'tabulate>=0.9.0,<0.10.0',
 'yaspin>=2.2.0,<3.0.0']

entry_points = \
{'console_scripts': ['proxygen = proxygen_cli.cli.command_main:main']}

setup_kwargs = {
    'name': 'proxygen-cli',
    'version': '2.0.10',
    'description': "CLI for interacting with NHSD APIM's proxygen service",
    'long_description': '# proxygen-cli\n\n## Installation\n\nShould be as simple as\n```\npip install proxygen-cli\n```\nThe python package includes an execuatable `proxygen`.\nType `proxygen` to see a list of available commands.\n\n\n## Configuration\n\n### Credentials\n\nAll users should have individual credentials.\n`proxygen-cli` needs to know about them.\n\n```\nproxygen credentials set username <USERNAME>\nproxygen credentials set password <PASSWORD>\n```\n\nThe CLI has its own client credentials, which need to be input.\nContact `deathstar` squad or the `platforms-api-producer-support` slack channel to find out what they are.\n```\nproxgen credentials set client_id <CLIENT_ID>\nproxgen credentials set client_secret <CLIENT_SECRET>\n```\n\n\n### Settings\n`proxygen-cli` needs to know what API you are developing.\n\n```\nproxygen settings set api <API-NAME>\n```\nYour user must have permissions to manipulate instances/secrets/specs for the API you set here.\nIf you do not have sufficient permissions commands will fail.\nIf you believe your permissions are incorrect, contact the `platforms-api-producer-support` channel.\n\n## Commands\nCommands are documented inside the CLI itself.\nType `proxygen` to see a list of available commands.\n',
    'author': 'Ben Strutt',
    'author_email': 'ben.strutt1@nhs.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/NHSDigital/proxygen-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
