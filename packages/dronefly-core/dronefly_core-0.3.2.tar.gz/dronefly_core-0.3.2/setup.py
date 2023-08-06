# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['core',
 'core.clients',
 'core.commands',
 'core.formatters',
 'core.models',
 'core.parsers',
 'core.query',
 'core.utils']

package_data = \
{'': ['*']}

install_requires = \
['dateparser>=1.1.1,<2.0.0',
 'inflect>=5.3.0,<6.0.0',
 'pyinaturalist>=0.17,<0.19',
 'rich>=10.9,<14']

setup_kwargs = {
    'name': 'dronefly-core',
    'version': '0.3.2',
    'description': 'Core dronefly components',
    'long_description': "# Dronefly core\n\nThis is an incomplete rewrite of [Dronefly](https://dronefly.readthedocs.io)\nDiscord bot's core components. We're not yet making version guarantees until\nit is more usable.\n\n# Related packages\n\n## Dronefly command-line client\n\nThe [dronefly-cli](https://github.com/dronefly-garden/dronefly-cli) command-line\nclient will provide a standalone text user interface that can perform a usable\nsubset of Dronefly Discord bot's capabilities, built solely with Dronefly core.\n\n## Dronefly Discord bot\n\nDronefly Discord bot brings [iNaturalist](https://www.inaturalist.org) taxa,\nobservations, and other data from the site into conversations on the\n[Discord](https://discord.com) chat platform.\n",
    'author': 'Ben Armstrong',
    'author_email': 'synrg@debian.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<3.12',
}


setup(**setup_kwargs)
