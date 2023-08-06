# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['abm_colony_collection']

package_data = \
{'': ['*']}

install_requires = \
['networkx>=3.0,<4.0',
 'numpy>=1.23.4,<2.0.0',
 'pandas>=1.5.1,<2.0.0',
 'prefect>=2.6.0,<3.0.0',
 'scikit-image>=0.19.3,<0.20.0',
 'scipy>=1.9.3,<2.0.0']

setup_kwargs = {
    'name': 'abm-colony-collection',
    'version': '0.2.0',
    'description': 'Collection of tasks for analyzing colony dynamics.',
    'long_description': '[![Build Status](https://github.com/allen-cell-animated/abm-colony-collection/workflows/build/badge.svg)](https://github.com/allen-cell-animated/abm-colony-collection/actions?query=workflow%3Abuild)\n[![Codecov](https://img.shields.io/codecov/c/gh/allen-cell-animated/abm-colony-collection?token=YSWZXHUW1R)](https://codecov.io/gh/allen-cell-animated/abm-colony-collection)\n[![Lint Status](https://github.com/allen-cell-animated/abm-colony-collection/workflows/lint/badge.svg)](https://github.com/allen-cell-animated/abm-colony-collection/actions?query=workflow%3Alint)\n[![Documentation](https://github.com/allen-cell-animated/abm-colony-collection/workflows/documentation/badge.svg)](https://allen-cell-animated.github.io/abm-colony-collection/)\n[![Code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n',
    'author': 'Jessica S. Yu',
    'author_email': 'jesyu@uw.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
