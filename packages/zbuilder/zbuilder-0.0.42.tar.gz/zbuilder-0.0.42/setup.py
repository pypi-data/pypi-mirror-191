# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zbuilder', 'zbuilder.dns', 'zbuilder.ipam', 'zbuilder.vm']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.0,<4.0',
 'PyJWT>=2.5.0,<3.0.0',
 'ansible>=7.0,<8.0',
 'arrow>=1.1,<2.0',
 'azure-mgmt-compute>=21.0,<22.0',
 'azure-mgmt-dns>=8.0,<9.0',
 'azure-mgmt-network>=19.0,<20.0',
 'azure-mgmt-resource>=18.0,<19.0',
 'boto3>=1.17,<2.0',
 'click>=8,<9',
 'colorama>=0.4,<0.5',
 'delegator.py>=0.1.1,<0.2.0',
 'dnspython>=2,<3',
 'dpath>=2.0,<3.0',
 'google-api-python-client>=2.9,<3.0',
 'google-auth-oauthlib>=0.4,<0.5',
 'google-cloud-dns>=0.32,<0.33',
 'massedit>=0.69,<0.70',
 'msrestazure>=0.6.4,<0.7.0',
 'oauthlib>=3.2.1,<4.0.0',
 'proxmoxer>=1.1,<2.0',
 'python-digitalocean>=1.16,<2.0',
 'requests>=2,<3',
 'retrying>=1.3,<2.0',
 'ruamel.yaml>=0.17,<0.18',
 'tabulate>=0.8,<0.9']

entry_points = \
{'console_scripts': ['zbuilder = zbuilder.cli:cli']}

setup_kwargs = {
    'name': 'zbuilder',
    'version': '0.0.42',
    'description': 'Create VMs',
    'long_description': '# Zbuilder: Building VMs and applying ansible playbooks\n\n[![PyPi version](https://badge.fury.io/py/zbuilder.svg)](https://pypi.org/project/zbuilder/)\n[![PyPi downloads](https://img.shields.io/pypi/dm/zbuilder.svg)](https://pypistats.org/packages/zbuilder)\n[![Build status](https://github.com/hasiotis/zbuilder/workflows/Build%20status/badge.svg)](https://github.com/hasiotis/zbuilder/actions?query=workflow%3A%22Build+status%22)\n[![Documentation Status](https://readthedocs.org/projects/zbuilder/badge/?version=stable)](https://zbuilder.readthedocs.io/en/develop/?badge=develop)\n[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://github.com/hasiotis/zbuilder/blob/master/LICENSE)\n\nZBuilder is a tool to help you build VMs ready to be transfered to ansible.\nBy using ansible as a library, it has access to all ansible variables. This\nway it achieves high integration with ansible.\n\n## Installation\n\nInstall and update using:\n```\npip3 install --user --upgrade zbuilder\n```\n\n## Links\n\n* [Documentation](https://zbuilder.readthedocs.io/en/stable/?badge=stable)\n* [Releases](https://pypi.org/project/zbuilder/)\n* [Code](https://github.com/hasiotis/zbuilder)\n',
    'author': 'Chasiotis Nikos',
    'author_email': 'hasiotis@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/hasiotis/zbuilder',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4',
}


setup(**setup_kwargs)
