# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['calitp_data']

package_data = \
{'': ['*']}

install_requires = \
['fsspec==2022.5.0', 'gcsfs==2022.5.0']

setup_kwargs = {
    'name': 'calitp-data',
    'version': '2023.2.13.1',
    'description': 'Shared code for the Cal-ITP data codebases',
    'long_description': 'None',
    'author': 'Andrew Vaccaro',
    'author_email': 'andrew.v@jarv.us',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
