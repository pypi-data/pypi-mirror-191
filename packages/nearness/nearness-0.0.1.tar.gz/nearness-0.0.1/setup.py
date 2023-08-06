# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nearness']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'nearness',
    'version': '0.0.1',
    'description': 'Flexible distance-based machine learning.',
    'long_description': '<p align="center">\n  nearest\n</p>\n',
    'author': 'David Muhr',
    'author_email': 'muhrdavid+github@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/davnn/nearest',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
