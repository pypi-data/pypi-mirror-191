# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['openlabels']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'openlabels',
    'version': '0.0.1',
    'description': '',
    'long_description': '# openlabel',
    'author': 'Jonatas Grosman',
    'author_email': 'jonatasgrosman@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
