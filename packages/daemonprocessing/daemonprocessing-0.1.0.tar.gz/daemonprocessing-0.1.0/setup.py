# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['daemonprocessing']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'daemonprocessing',
    'version': '0.1.0',
    'description': 'cross-platform daemon',
    'long_description': 'cross-platform daemon',
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
