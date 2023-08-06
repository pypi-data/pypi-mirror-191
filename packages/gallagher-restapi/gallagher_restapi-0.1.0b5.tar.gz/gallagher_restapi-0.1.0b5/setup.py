# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gallagher_restapi']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.3,<0.24.0', 'pytz>=2022.7.1,<2023.0.0']

setup_kwargs = {
    'name': 'gallagher-restapi',
    'version': '0.1.0b5',
    'description': '',
    'long_description': 'None',
    'author': 'Rami Mosleh',
    'author_email': 'engrbm87@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
