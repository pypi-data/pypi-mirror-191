# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydlj', 'pydlj.shorteners']

package_data = \
{'': ['*']}

install_requires = \
['codefast>=0.9.23,<0.10.0']

setup_kwargs = {
    'name': 'pydlj',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
