# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pmcrypt']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pmcrypt',
    'version': '0.1.0',
    'description': 'A Python package to properly handle passwords',
    'long_description': '# pmcrypt\n\nHandle passwords safely with pmcrypt!\n',
    'author': 'Vitaman02',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
