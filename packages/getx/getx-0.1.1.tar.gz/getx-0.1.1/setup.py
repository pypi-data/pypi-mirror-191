# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['getx']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=39.0.1,<40.0.0', 'requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'getx',
    'version': '0.1.1',
    'description': '',
    'long_description': '',
    'author': 'Elsafy Hegazy',
    'author_email': 'safy.dev@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
