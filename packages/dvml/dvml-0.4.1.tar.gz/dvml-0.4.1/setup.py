# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dvml', 'dvml.metrics', 'dvml.models', 'dvml.optimization', 'dvml.utils']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.24.1,<2.0.0']

setup_kwargs = {
    'name': 'dvml',
    'version': '0.4.1',
    'description': '',
    'long_description': '# DVML\n\n> Toy package to practice implementing ML models from scratch. Not a serious project.\n\n[![PyPI Version][pypi-image]][pypi-url]\n[![Build Status][build-image]][build-url]\n[![Code Coverage][coverage-image]][coverage-url]\n[![][versions-image]][versions-url]\n\n<!-- Badges: -->\n\n[pypi-image]: https://img.shields.io/pypi/v/dvml\n[pypi-url]: https://pypi.org/project/dvml\n[build-image]: https://github.com/viegasdll/dvml/actions/workflows/build.yaml/badge.svg\n[build-url]: https://github.com/viegasdll/dvml/actions/workflows/build.yaml\n[coverage-image]: https://codecov.io/gh/viegasdll/dvml/branch/main/graph/badge.svg\n[coverage-url]: https://codecov.io/gh/viegasdll/dvml\n[versions-image]: https://img.shields.io/pypi/pyversions/dvml\n[versions-url]: https://pypi.org/project/dvml\n',
    'author': 'Daniel Viegas',
    'author_email': 'viegasdll@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
