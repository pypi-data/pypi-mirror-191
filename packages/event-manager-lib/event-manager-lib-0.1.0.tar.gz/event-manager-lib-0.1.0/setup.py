# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['event_manager_lib']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'event-manager-lib',
    'version': '0.1.0',
    'description': 'Event/ State Manager library/ SDK',
    'long_description': None,
    'author': 'David Lubomirov',
    'author_email': 'davidlubomirov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8.0,<3.9.0',
}


setup(**setup_kwargs)
