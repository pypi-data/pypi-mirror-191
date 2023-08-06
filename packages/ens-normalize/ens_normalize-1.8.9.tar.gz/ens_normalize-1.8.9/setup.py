# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ens_normalize']

package_data = \
{'': ['*']}

install_requires = \
['pyunormalize>=15.0.0,<16.0.0', 'regex>=2022.10.31,<2023.0.0']

setup_kwargs = {
    'name': 'ens-normalize',
    'version': '1.8.9',
    'description': 'ES6 Ethereum Name Service (ENS) Name Normalizer',
    'long_description': '# ENS Normalize\n\nBased on JavaScript implementation version [1.8.9](https://github.com/adraffy/ens-normalize.js/tree/fa0ad385e77299ad8bddc2287876fbf74a92b8db)\n',
    'author': 'Jakub Karbowski',
    'author_email': 'carbon225@proton.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
