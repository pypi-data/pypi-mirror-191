# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['calitp']

package_data = \
{'': ['*']}

install_requires = \
['fsspec==2022.5.0', 'gcsfs==2022.5.0']

setup_kwargs = {
    'name': 'calitp',
    'version': '2023.2.10',
    'description': 'Shared code for the Cal-ITP data codebases',
    'long_description': 'None',
    'author': 'Andrew Vaccaro',
    'author_email': 'atvaccaro@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
