# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['archimedes',
 'archimedes.data',
 'archimedes.data.api',
 'archimedes.testdata',
 'archimedes.utils',
 'archimedes.utils.split']

package_data = \
{'': ['*'], 'archimedes.testdata': ['datasets/*']}

install_requires = \
['cachetools>=5.2.0,<6.0.0',
 'iteration-utilities>=0.11.0,<0.12.0',
 'msal-extensions>=1.0.0,<2.0.0',
 'msal>=1.10.0,<2.0.0',
 'pandas>=1.0.5',
 'requests>=2.27.0',
 'retry>=0.9.2,<0.10.0']

setup_kwargs = {
    'name': 'archimedes-python-client',
    'version': '4.15.2',
    'description': 'The Python library for Archimedes',
    'long_description': 'None',
    'author': 'Optimeering AS',
    'author_email': 'dev@optimeering.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.12',
}


setup(**setup_kwargs)
