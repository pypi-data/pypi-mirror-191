# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['reconlib',
 'reconlib.core',
 'reconlib.core.utils',
 'reconlib.crtsh',
 'reconlib.hackertarget',
 'reconlib.virustotal']

package_data = \
{'': ['*']}

install_requires = \
['python-dotenv>=0.21.1,<0.22.0']

setup_kwargs = {
    'name': 'reconlib',
    'version': '0.4.4',
    'description': 'A collection of modules and helpers for active and passive reconnaissance of remote hosts',
    'long_description': 'None',
    'author': 'eonraider',
    'author_email': 'livewire_voodoo@protonmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
