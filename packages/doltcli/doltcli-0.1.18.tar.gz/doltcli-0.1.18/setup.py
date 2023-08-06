# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['doltcli']

package_data = \
{'': ['*']}

install_requires = \
['typed-ast>1.4.3']

extras_require = \
{':python_version < "3.7"': ['dataclasses>=0.6']}

setup_kwargs = {
    'name': 'doltcli',
    'version': '0.1.18',
    'description': "Slim Python interface for Dolt's CLI API.",
    'long_description': 'None',
    'author': 'Max Hoffman',
    'author_email': 'max@dolthub.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.2,<4.0',
}


setup(**setup_kwargs)
