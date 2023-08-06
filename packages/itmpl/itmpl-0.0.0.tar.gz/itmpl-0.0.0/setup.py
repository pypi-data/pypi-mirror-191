# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['itmpl']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'itmpl',
    'version': '0.0.0',
    'description': 'A project templating and scaffolding tool',
    'long_description': '# itmpl\nA project templating and scaffolding tool built in Python\n',
    'author': 'Isaac Harris-Holt',
    'author_email': 'isaac@harris-holt.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
