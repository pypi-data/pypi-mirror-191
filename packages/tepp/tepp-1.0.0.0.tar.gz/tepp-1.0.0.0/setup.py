# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tepp']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tepp',
    'version': '1.0.0.0',
    'description': 'The Extension Pure Python',
    'long_description': 'The Extension Pure Python',
    'author': 'XXIMDE',
    'author_email': 'xximde@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
}


setup(**setup_kwargs)
