# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['transactions',
 'transactions.common',
 'transactions.common.schema',
 'transactions.types',
 'transactions.types.assets',
 'transactions.types.elections']

package_data = \
{'': ['*'], 'transactions.common.schema': ['v1.0/*', 'v2.0/*', 'v3.0/*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'base58>=2.1.1,<3.0.0',
 'jsonschema>=4.16.0,<5.0.0',
 'planetmint-cryptoconditions>=1.1.0,<2.0.0',
 'planetmint-ipld>=0.0.3,<0.0.4',
 'planetmint-py-cid>=0.4.2,<0.5.0',
 'python-rapidjson>=1.8,<2.0']

setup_kwargs = {
    'name': 'planetmint-transactions',
    'version': '0.7.0',
    'description': 'Python implementation of the planetmint transactions spec',
    'long_description': '# transactions\nPython implementation of the planetmint transactions spec\n',
    'author': 'Lorenz Herzberger',
    'author_email': 'lorenzherzberger@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
