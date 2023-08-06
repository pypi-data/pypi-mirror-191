# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['resourcesing']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'resourcesing',
    'version': '0.1.1',
    'description': '',
    'long_description': '',
    'author': 'jawide',
    'author_email': '596929059@qq.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
