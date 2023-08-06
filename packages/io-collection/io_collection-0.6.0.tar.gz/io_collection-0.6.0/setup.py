# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['io_collection',
 'io_collection.keys',
 'io_collection.load',
 'io_collection.quilt',
 'io_collection.save']

package_data = \
{'': ['*']}

install_requires = \
['aicsimageio>=4.9.2,<5.0.0',
 'boto3>=1.24.59,<2.0.0',
 'matplotlib>=3.6.1,<4.0.0',
 'numpy>=1.23.4,<2.0.0',
 'pandas>=1.5.1,<2.0.0',
 'prefect>=2.6.0,<3.0.0',
 'quilt3>=5.0.0,<6.0.0',
 's3fs>=2022.10.0,<2023.0.0']

setup_kwargs = {
    'name': 'io-collection',
    'version': '0.6.0',
    'description': 'Collection of tasks for I/O.',
    'long_description': '[![Build Status](https://github.com/allen-cell-animated/io-collection/workflows/build/badge.svg)](https://github.com/allen-cell-animated/io-collection/actions?query=workflow%3Abuild)\n[![Codecov](https://img.shields.io/codecov/c/gh/allen-cell-animated/io-collection?token=KQTGXCOLLU)](https://codecov.io/gh/allen-cell-animated/io-collection)\n[![Lint Status](https://github.com/allen-cell-animated/io-collection/workflows/lint/badge.svg)](https://github.com/allen-cell-animated/io-collection/actions?query=workflow%3Alint)\n[![Documentation](https://github.com/allen-cell-animated/io-collection/workflows/documentation/badge.svg)](https://allen-cell-animated.github.io/io-collection/)\n[![Code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n',
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
