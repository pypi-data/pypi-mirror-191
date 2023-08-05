# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['justmydemo']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'justmydemo',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Ubuntu20',
    'author_email': 'xxx@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
