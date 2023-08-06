# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pd_extras', 'pd_extras.check', 'pd_extras.extra', 'pd_extras.optimize']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.5.3']

setup_kwargs = {
    'name': 'pd-extras',
    'version': '3.1.6',
    'description': 'Some utility functions on top of pandas.',
    'long_description': '# Pandas Utilities\n\n![Build](https://github.com/proafxin/pandas-utils/actions/workflows/tox_build.yml/badge.svg)\n![Workflow for Codecov Action](https://github.com/proafxin/pd-extras/actions/workflows/codecov.yml/badge.svg)\n[![codecov](https://codecov.io/gh/proafxin/pd-extras/branch/develop/graph/badge.svg?token=AQA0IJY4N1)](https://codecov.io/gh/proafxin/pd-extras)[![Documentation Status](https://readthedocs.org/projects/pd-extras/badge/?version=latest)](https://pd-extras.readthedocs.io/en/latest/?badge=latest)\n\nSome functions on top of pandas.\n',
    'author': 'Masum Billal',
    'author_email': 'billalmasum93@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/proafxin/pandas-utils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
