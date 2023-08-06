# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xata', 'xata.namespaces', 'xata.namespaces.core', 'xata.namespaces.workspace']

package_data = \
{'': ['*']}

install_requires = \
['orjson>=3.8.1,<4.0.0',
 'python-dotenv>=0.21.0,<0.22.0',
 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'xata',
    'version': '0.2.1',
    'description': 'Python client for Xata.io',
    'long_description': '<p align="center">\n  <img width="200" src="https://raw.githubusercontent.com/xataio/company/main/logo/non-resizable/for-light-backgrounds/colored-with-text.png#gh-light-mode-only" />\n  <img width="200" src="https://raw.githubusercontent.com/xataio/company/main/logo/non-resizable/for-dark-backgrounds/colored-with-text.png#gh-dark-mode-only" />\n</p>\n\n# Python SDK for Xata\n\n[![Documentation Status](https://readthedocs.org/projects/xata-py/badge/?version=latest)](https://xata-py.readthedocs.io/en/latest/?badge=latest) [![PyPI version](https://badge.fury.io/py/xata.svg)](https://badge.fury.io/py/xata)\n\nSimple Python client for xata.io databases. Currently work in progress.\n\nXata is a Serverless Database that is as easy to use as a spreadsheet, has the\ndata integrity of PostgreSQL, and the search and analytics functionality of\nElasticsearch.\n\nThe Python SDK uses type annotations and requires Python 3.8 or higher.\n\nTo install, run:\n\n```\npip install xata\n```\n\nTo learn more about Xata, visit [xata.io](https://xata.io).\n\n- Python client documentation: https://xata-py.readthedocs.io\n- API Reference: https://xata-py.readthedocs.io/en/latest/api.html\n',
    'author': 'Xata',
    'author_email': 'support@xata.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
