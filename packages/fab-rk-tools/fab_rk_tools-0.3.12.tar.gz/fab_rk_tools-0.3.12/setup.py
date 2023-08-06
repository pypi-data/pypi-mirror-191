# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fab_rk_tools',
 'fab_rk_tools.assets',
 'fab_rk_tools.common',
 'fab_rk_tools.data',
 'fab_rk_tools.data.test',
 'fab_rk_tools.exceptions',
 'fab_rk_tools.graphs',
 'fab_rk_tools.stats']

package_data = \
{'': ['*']}

install_requires = \
['archimedes-python-client', 'numpy', 'pandas', 'plotly']

setup_kwargs = {
    'name': 'fab-rk-tools',
    'version': '0.3.12',
    'description': 'Common tools and utilities for RK graphs',
    'long_description': 'None',
    'author': 'Optimeering AS',
    'author_email': 'dev@optimeering.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.12',
}


setup(**setup_kwargs)
