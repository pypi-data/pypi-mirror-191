# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fluxvault']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=22.1.0,<23.0.0',
 'aiohttp>=3.8.3,<4.0.0',
 'aioshutil>=1.2,<2.0',
 'dnspython>=2.2.1,<3.0.0',
 'fluxrpc[socket]>=0.9.5,<0.10.0',
 'fluxwallet>=0.0.2,<0.0.3',
 'keyring>=23.11.0,<24.0.0',
 'ownca>=0.3.3,<0.4.0',
 'python-daemon>=2.3.2,<3.0.0',
 'python-socketio>=5.7.2,<6.0.0',
 'pyyaml>=6.0,<7.0',
 'randomname>=0.1.5,<0.2.0',
 'requests>=2.28.1,<3.0.0',
 'rich>=12.6.0,<13.0.0',
 'show-in-file-manager>=1.1.4,<2.0.0',
 'typer>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['fluxvault = fluxvault.cli:entrypoint']}

setup_kwargs = {
    'name': 'fluxvault',
    'version': '0.7.5',
    'description': 'A system to load secrets into Flux applications',
    'long_description': 'None',
    'author': 'David White',
    'author_email': 'dr.white.nz@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://runonflux.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
