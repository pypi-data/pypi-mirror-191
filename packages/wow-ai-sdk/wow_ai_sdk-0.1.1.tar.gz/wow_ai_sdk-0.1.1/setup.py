# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wow_ai_sdk']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'wow-ai-sdk',
    'version': '0.1.1',
    'description': '',
    'long_description': 'wow ai sdk',
    'author': 'TonyShark',
    'author_email': 'quoi@wow-ai.inc',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
