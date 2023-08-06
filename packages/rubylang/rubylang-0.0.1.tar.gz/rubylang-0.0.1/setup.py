# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rubylang']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'rubylang',
    'version': '0.0.1',
    'description': 'Ruby like objects in Python',
    'long_description': "# rubylang - Ruby like objects in Python\n\nGet Ruby's Hash, Array or String like objects in Python.\n",
    'author': 'Sumanth',
    'author_email': 'sumanthreddystar@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
