# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tabletoppy']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tabletoppy',
    'version': '0.1.0',
    'description': 'A Python library for simulating tabletop games, including dice rolls, coin tosses etc.',
    'long_description': '[![code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![docs: passing](https://readthedocs.org/projects/tabletoppy/badge/?version=latest)](https://tabletoppy.readthedocs.io/en/latest/?badge=latest)\n\n# Tabletoppy\n\nA Python library for simulating tabletop games, including dice rolls, coin tosses etc.\n',
    'author': 'peaky76',
    'author_email': 'robertjamespeacock@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
